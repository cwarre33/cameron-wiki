#!/usr/bin/env python3
"""
WOW Recon Session - High-Value Secret Discovery

This script runs targeted searches for exposed credentials in public GitHub repos,
then uses TruffleHog to extract actual secrets from the most promising targets.

Usage:
    export GITHUB_PAT="your_github_pat"
    python wow_recon_session.py
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Configuration
HIGH_VALUE_PATTERNS = [
    {"query": "filename:.env mongodb+srv", "desc": "MongoDB connection strings"},
    {"query": "filename:.env AWS_ACCESS_KEY", "desc": "AWS credentials"},
    {"query": "filename:.env OPENAI_API_KEY", "desc": "OpenAI API keys"},
    {"query": "filename:.env SLACK_TOKEN", "desc": "Slack tokens"},
    {"query": "filename:.env DATABASE_URL postgres", "desc": "PostgreSQL databases"},
    {"query": "filename:config.json stripe sk_live", "desc": "Stripe API keys"},
    {"query": "filename:.env private_key", "desc": "Private keys"},
    {"query": "filename:.env jwt_secret", "desc": "JWT secrets"},
]

class WOWRecon:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.discoveries = []
        self.repos_scanned = []
        
    def search_repos(self, query, max_results=10):
        """Search GitHub for code matching pattern"""
        url = f"https://api.github.com/search/code"
        params = {
            'q': query,
            'sort': 'indexed',
            'order': 'desc',
            'per_page': max_results
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"  ❌ Error searching: {e}")
            return {'total_count': 0, 'items': []}
    
    def clone_and_scan(self, repo_url, clone_dir="/tmp/trufflehog_scans"):
        """Clone repo and run TruffleHog"""
        Path(clone_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = f"{clone_dir}/{repo_name}"
        
        # Clean up old clone
        if os.path.exists(repo_path):
            subprocess.run(['rm', '-rf', repo_path], check=False)
        
        # Clone
        try:
            clone_result = subprocess.run(
                ['git', 'clone', '--depth', '50', '--single-branch', repo_url, repo_path],
                capture_output=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Clone timeout, skipping...")
            return None
        
        if clone_result.returncode != 0:
            return None
        
        # Run TruffleHog
        config_path = "trufflehog-config.yml"
        th_cmd = [
            'trufflehog', 'filesystem', repo_path,
            '--json', '--no-update',
            '--config', config_path
        ] if os.path.exists(config_path) else [
            'trufflehog', 'filesystem', repo_path,
            '--json', '--no-update'
        ]
        
        th_result = subprocess.run(th_cmd, capture_output=True, text=True)
        
        findings = []
        for line in th_result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    findings.append(json.loads(line))
                except:
                    pass
        
        # Cleanup
        subprocess.run(['rm', '-rf', repo_path], check=False)
        
        return findings
    
    def run_discovery(self):
        """Run the full discovery workflow"""
        print("🌟" * 40)
        print("          WOW DISCOVERY SESSION")
        print(f"          Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌟" * 40)
        print()
        
        all_targets = []
        
        for pattern in HIGH_VALUE_PATTERNS:
            print(f"🔍 Searching: {pattern['desc']}")
            print(f"   Query: {pattern['query']}")
            
            results = self.search_repos(pattern['query'], max_results=8)
            total = results.get('total_count', 0)
            items = results.get('items', [])
            
            print(f"   Found: {total:,} total matches")
            
            for item in items[:5]:  # Top 5 from each pattern
                repo = item['repository']['full_name']
                path = item['path']
                all_targets.append({
                    'repo': repo,
                    'path': path,
                    'html_url': item['html_url'],
                    'score': self._calc_priority(repo, path, pattern['desc'])
                })
        
        # Deduplicate and sort by priority
        seen = set()
        unique_targets = []
        for t in sorted(all_targets, key=lambda x: x['score'], reverse=True):
            key = t['repo']
            if key not in seen:
                seen.add(key)
                unique_targets.append(t)
        
        print(f"\n🎯 Selected {len(unique_targets)} unique repos for deep scan")
        print()
        
        # Deep scan top targets
        for target in unique_targets[:5]:
            print(f"🔬 Scanning: {target['repo']}")
            print(f"   Priority score: {target['score']}")
            
            # Clone URL
            clone_url = f"https://github.com/{target['repo']}.git"
            
            findings = self.clone_and_scan(clone_url)
            
            if findings:
                print(f"   ⚠️  FOUND {len(findings)} SECRET(S)!")
                for finding in findings:
                    detector = finding.get('DetectorName', 'unknown')
                    raw = finding.get('Raw', 'REDACTED')[:30] + "..." if finding.get('Raw') else 'N/A'
                    print(f"      → {detector}: {raw}")
                    self.discoveries.append({
                        'repo': target['repo'],
                        'detector': detector,
                        'file': finding.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('file', 'unknown'),
                        'found_at': datetime.now().isoformat()
                    })
            else:
                print(f"   ✅ Clean or scan failed")
            
            print()
        
        # Report
        print("=" * 60)
        print("DISCOVERY SUMMARY")
        print("=" * 60)
        print(f"Patterns searched: {len(HIGH_VALUE_PATTERNS)}")
        print(f"Repos deep-scanned: {len(unique_targets[:5])}")
        print(f"Secrets discovered: {len(self.discoveries)}")
        
        if self.discoveries:
            print("\n🚨 DISCOVERED SECRETS:")
            for d in self.discoveries:
                print(f"   {d['repo']}: {d['detector']}")
        
        # Save report
        report_path = f"reports/wow_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'discoveries': self.discoveries,
                'targets_scanned': len(unique_targets[:5]),
                'patterns': HIGH_VALUE_PATTERNS
            }, f, indent=2)
        
        print(f"\n📄 Report saved: {report_path}")
        
    def _calc_priority(self, repo, path, desc):
        """Calculate priority score for a target"""
        score = 0
        
        # Path-based scoring
        if '.env' in path: score += 10
        if 'config' in path.lower(): score += 5
        if 'prod' in path.lower(): score += 15
        if 'secret' in path.lower(): score += 8
        
        # Description scoring
        if 'database' in desc.lower(): score += 10
        if 'aws' in desc.lower(): score += 12
        if 'stripe' in desc.lower(): score += 15
        if 'private_key' in desc.lower(): score += 20
        
        # Repo indicators
        if 'test' not in repo.lower() and 'example' not in repo.lower():
            score += 5
        
        return score

if __name__ == '__main__':
    import sys
    
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Please set GITHUB_PAT environment variable")
        print("   export GITHUB_PAT='your_github_pat'")
        sys.exit(1)
    
    recon = WOWRecon()
    recon.run_discovery()
