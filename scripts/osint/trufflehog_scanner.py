#!/usr/bin/env python3
"""
TruffleHog + GitHub Scanner

Clones repos with exposed secrets and runs TruffleHog against them.
Uses your GitHub PAT to find repos, then TruffleHog to extract secrets.
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
import urllib.request

# High-yield patterns
TARGET_PATTERNS = [
    "AKIA",                    # AWS
    "AIzaS",                   # Google
    "mongodb+srv://",          # MongoDB
    "sk_live_",                # Stripe
    "xoxb-",                   # Slack
    "ghp_",                    # GitHub
]


def get_github_pat():
    """Get GitHub PAT from environment"""
    return os.environ.get("GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")


def search_github(pattern, pat, per_page=10):
    """Search GitHub for repos with exposed secrets"""
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    url = f"https://api.github.com/search/code?q={pattern}&per_page={per_page}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error searching for {pattern}: {e}")
        return {"items": []}


def clone_repo(repo_url, dest):
    """Clone a GitHub repo"""
    try:
        subprocess.run(
            ["git", "clone", "--depth", "20", repo_url, dest],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return True
    except Exception as e:
        print(f"Error cloning {repo_url}: {e}")
        return False


def run_trufflehog(repo_path, config_path="./trufflehog-config.yml"):
    """Run TruffleHog on cloned repo"""
    try:
        cmd = [
            "trufflehog",
            "filesystem",
            repo_path,
            "--config", config_path,
            "--json",
            "--no-update",
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        # Parse JSON results
        findings = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    findings.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        
        return findings
        
    except FileNotFoundError:
        print("TruffleHog not installed. Install with:")
        print("  brew install trufflesecurity/trufflehog/trufflehog")
        print("  OR")
        print("  curl -sSfL https://install.trufflehog.org | sh")
        return []
    except Exception as e:
        print(f"Error running TruffleHog: {e}")
        return []


def scan_repos(patterns, pat, max_repos=5):
    """Full pipeline: search → clone → scan"""
    print("="*70)
    print("TRUFFLEHOG + GITHUB SCAN")
    print("="*70)
    print()
    
    all_findings = []
    scanned_repos = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for pattern in patterns:
            print(f"\n🔍 Searching for pattern: {pattern}")
            results = search_github(pattern, pat)
            
            items = results.get("items", [])
            print(f"   Found {len(items)} code matches")
            
            # Get unique repos
            repos_seen = set()
            repos_to_scan = []
            
            for item in items:
                repo = item.get("repository", {})
                repo_name = repo.get("full_name")
                if repo_name and repo_name not in repos_seen:
                    repos_seen.add(repo_name)
                    clone_url = repo.get("clone_url")
                    if clone_url:
                        repos_to_scan.append((repo_name, clone_url))
                
                if len(repos_to_scan) >= max_repos:
                    break
            
            print(f"   Sampling {len(repos_to_scan)} repos for TruffleHog scan...")
            
            for repo_name, clone_url in repos_to_scan:
                print(f"\n   📦 {repo_name}")
                
                # Clone
                clone_dest = Path(tmpdir) / repo_name.replace("/", "_")
                if clone_repo(clone_url, str(clone_dest)):
                    print("      ✅ Cloned")
                    
                    # Scan with TruffleHog
                    findings = run_trufflehog(str(clone_dest))
                    if findings:
                        print(f"      💥 Found {len(findings)} secrets!")
                        all_findings.extend(findings)
                    else:
                        print("      (No secrets found)")
                    
                    scanned_repos.append(repo_name)
                else:
                    print("      ❌ Failed to clone")
    
    return all_findings, scanned_repos


def generate_report(findings, scanned_repos, out_file="trufflehog-findings.json"):
    """Generate JSON report"""
    report = {
        "scan_time": datetime.now().isoformat(),
        "tool": "trufflehog",
        "repos_scanned": len(scanned_repos),
        "total_findings": len(findings),
        "scanned_repos": scanned_repos,
        "findings": findings,
    }
    
    Path(out_file).write_text(json.dumps(report, indent=2))
    print(f"\n✅ Report saved: {out_file}")
    
    return report


def main():
    pat = get_github_pat()
    if not pat:
        print("Error: Set GITHUB_PAT environment variable")
        sys.exit(1)
    
    # Run scan
    findings, scanned_repos = scan_repos(TARGET_PATTERNS, pat, max_repos=3)
    
    # Generate report
    report = generate_report(findings, scanned_repos)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Repos scanned: {len(scanned_repos)}")
    print(f"Total secrets found: {len(findings)}")
    
    if findings:
        print("\n⚠️ SECRETS FOUND!")
        print("Review trufflehog-findings.json for details")


if __name__ == "__main__":
    main()
