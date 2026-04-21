#!/usr/bin/env python3
"""
GitHub Secret Monitor - Daily OSINT Scanner

This script searches GitHub for exposed secrets and generates a daily report.
Designed to run as a GitHub Action or cron job.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Patterns to monitor
SECRET_PATTERNS = {
    "aws_access_keys": {
        "query": "AKIA",
        "description": "AWS Access Key IDs",
        "severity": "CRITICAL",
    },
    "google_api_keys": {
        "query": "AIzaS",
        "description": "Google API Keys",
        "severity": "CRITICAL",
    },
    "private_keys": {
        "query": "BEGIN RSA PRIVATE KEY",
        "description": "RSA Private Keys",
        "severity": "CRITICAL",
    },
    "db_passwords": {
        "query": "password= language:python",
        "description": "Database Passwords",
        "severity": "HIGH",
    },
    "api_keys_generic": {
        "query": "api_key language:python",
        "description": "Generic API Keys",
        "severity": "HIGH",
    },
    "slack_tokens": {
        "query": "xoxb-",
        "description": "Slack Bot Tokens",
        "severity": "MEDIUM",
    },
    "stripe_keys": {
        "query": "sk_live_",
        "description": "Stripe Live Keys",
        "severity": "CRITICAL",
    },
    "firebase_urls": {
        "query": "firebaseio.com",
        "description": "Firebase Database URLs",
        "severity": "MEDIUM",
    },
    "mongodb_uris": {
        "query": "mongodb+srv://",
        "description": "MongoDB Connection URIs",
        "severity": "CRITICAL",
    },
    "mysql_connections": {
        "query": "mysql://",
        "description": "MySQL Connection Strings",
        "severity": "CRITICAL",
    },
}

COMMIT_PATTERNS = {
    "passwords_removed": "remove password",
    "api_keys_deleted": "delete api key",
    "secrets_fixed": "fix secret",
    "credentials_removed": "remove credentials",
    "tokens_deleted": "delete token",
    "sensitive_data_removed": "remove sensitive",
}


def get_github_pat():
    """Get GitHub PAT from environment"""
    pat = os.environ.get("GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")
    if not pat:
        print("Error: GITHUB_PAT environment variable not set", file=sys.stderr)
        sys.exit(1)
    return pat


def make_github_request(url, headers):
    """Make authenticated GitHub API request"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode()), dict(resp.headers)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {"error": "rate_limited"}, {}
        elif e.code == 401:
            return {"error": "unauthorized"}, {}
        return {"error": f"HTTP_{e.code}"}, {}
    except Exception as e:
        return {"error": str(e)}, {}


def scan_code_patterns(pat):
    """Search GitHub for exposed secrets in code"""
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OSINT-Secret-Monitor",
    }
    
    results = {}
    total_findings = 0
    
    print("🔍 Scanning GitHub for exposed secrets in code...")
    
    for name, config in SECRET_PATTERNS.items():
        query = config["query"]
        url = f"https://api.github.com/search/code?q={query.replace(' ', '+')}&per_page=1"
        
        data, resp_headers = make_github_request(url, headers)
        
        if "error" in data:
            results[name] = {
                "count": 0,
                "status": data["error"],
                "severity": config["severity"],
            }
        else:
            count = data.get("total_count", 0)
            results[name] = {
                "count": count,
                "status": "found",
                "severity": config["severity"],
                "description": config["description"],
            }
            total_findings += count
            
        print(f"   {config['description']:40} {results[name].get('count', 0):>10,}")
    
    return results, total_findings


def scan_commit_history(pat):
    """Search GitHub commits for secret removal patterns"""
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.cloak-preview",
        "User-Agent": "OSINT-Secret-Monitor",
    }
    
    results = {}
    
    print("\n🔍 Scanning GitHub commit history for secret removals...")
    
    for name, query in COMMIT_PATTERNS.items():
        url = f"https://api.github.com/search/commits?q={query.replace(' ', '+')}&per_page=1"
        
        data, _ = make_github_request(url, headers)
        
        if "error" in data:
            results[name] = {"count": 0, "status": data["error"]}
        else:
            count = data.get("total_count", 0)
            results[name] = {"count": count, "status": "found"}
            
        print(f"   {name.replace('_', ' ').title():40} {results[name].get('count', 0):>10,}")
    
    return results


def get_rate_limit(pat):
    """Check GitHub API rate limits"""
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    url = "https://api.github.com/rate_limit"
    data, _ = make_github_request(url, headers)
    
    return data.get("resources", {})


def generate_report(code_results, commit_results, rate_limit, total_findings):
    """Generate markdown report"""
    now = datetime.now()
    
    report = f"""# 🔒 Secret Monitoring Report

**Generated:** {now.strftime("%Y-%m-%d %H:%M:%S UTC")}  
**Total Findings:** {total_findings:,}

---

## 📊 Exposed Secrets in Public Code

| Pattern | Count | Severity |
|---------|-------|----------|
"""
    
    for name, data in code_results.items():
        desc = data.get("description", name.replace("_", " ").title())
        count = data.get("count", 0)
        severity = data.get("severity", "UNKNOWN")
        emoji = "🔴" if severity == "CRITICAL" else "🟡" if severity == "HIGH" else "🟢"
        report += f"| {desc} | {count:,} | {emoji} {severity} |\n"
    
    report += """

---

## 🔍 Secret Removal History (Commits)

Developers who tried to remove secrets (may still be in git history):

| Pattern | Count |
|---------|-------|
"""
    
    for name, data in commit_results.items():
        count = data.get("count", 0)
        label = name.replace("_", " ").title()
        report += f"| {label} | {count:,} |\n"
    
    report += """

---

## ⚙️ Rate Limit Status

"""
    
    if rate_limit:
        search = rate_limit.get("search", {})
        core = rate_limit.get("core", {})
        report += f"""- **Search API:** {search.get('remaining', '?')}/{search.get('limit', '?')} remaining
- **Core API:** {core.get('remaining', '?')}/{core.get('limit', '?')} remaining
"""
    
    report += """

---

## 📈 Historical Trend

See [history](./history) for historical reports.

---

*This report was automatically generated by the OSINT Secret Monitor.*
"""
    
    return report


def save_report(report, out_dir="reports"):
    """Save report to file"""
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = out_path / f"{today}-report.md"
    report_file.write_text(report)
    
    # Also update latest
    latest = out_path / "README.md"
    latest.write_text(report)
    
    return report_file


def main():
    print("="*70)
    print("GITHUB SECRET MONITOR - Daily Scan")
    print("="*70)
    print()
    
    pat = get_github_pat()
    
    # Run scans
    code_results, total_findings = scan_code_patterns(pat)
    commit_results = scan_commit_history(pat)
    rate_limit = get_rate_limit(pat)
    
    # Generate report
    print("\n📄 Generating report...")
    report = generate_report(code_results, commit_results, rate_limit, total_findings)
    
    # Save report
    report_file = save_report(report)
    print(f"✅ Report saved: {report_file}")
    
    print()
    print("="*70)
    print(f"SUMMARY: {total_findings:,} total exposed secrets found")
    print("="*70)


if __name__ == "__main__":
    main()
