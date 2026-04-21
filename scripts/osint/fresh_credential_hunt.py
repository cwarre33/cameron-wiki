#!/usr/bin/env python3
"""
Fresh Credential Hunter - Target recent commits and specific files
Focus: .env files, config.json, credentials.json, recent pushes
"""

import requests
import re
import json
import os
from datetime import datetime, timedelta
from urllib.parse import quote

GITHUB_PAT = os.environ.get('GITHUB_PAT')
if not GITHUB_PAT:
    print("❌ Set GITHUB_PAT")
    exit(1)

HEADERS = {
    'Authorization': f'token {GITHUB_PAT}',
    'Accept': 'application/vnd.github.v3+json'
}

# Target: Recent commits with specific files
TARGETS = [
    "filename:.env.pushed:>2025-01-01",
    "filename:credentials.json pushed:>2025-01-01",
    "filename:config.json pushed:>2025-01-01",
    "filename:secrets.yml pushed:>2025-01-01",
    "filename:.aws/credentials pushed:>2025-01-01",
    "extension:key path:private",
    "AWS_ACCESS_KEY_ID pushed:>2025-04-01",
    "ghp_ pushed:>2025-04-01",
    "sk_live_ pushed:>2025-04-01",
]

# High-entropy patterns (real credentials, not examples)
PATTERNS = {
    'GitHub PAT': r'ghp_[a-zA-Z0-9]{36}',
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'AWS Secret': r'[0-9a-zA-Z/+]{40}',
    'Stripe Live': r'sk_live_[0-9a-zA-Z]{24,}',
    'Slack Token': r'xox[baprs]-[0-9a-zA-Z]{10,48}',
    'MongoDB URI': r'mongodb\+srv://[^\s\"]+:[^\s\"]+@[^\s\"]+\.mongodb\.net',
    'Private Key': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'Password in URL': r'https?://[^:]+:[^@\s\"]+@[^\s\"]+',
}

discoveries = []
files_checked = 0
max_discoveries = 5

print("=" * 60)
print("   FRESH CREDENTIAL HUNTER")
print("   Targeting recent commits & specific files")
print("=" * 60)
print()

for target in TARGETS:
    if len(discoveries) >= max_discoveries:
        break
    
    print(f"🔍 Searching: {target}")
    url = f"https://api.github.com/search/code?q={quote(target)}&sort=indexed&order=desc&per_page=10"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"   ⚠️ API error: {resp.status_code}")
            continue
        
        data = resp.json()
        items = data.get('items', [])
        print(f"   Found {len(items)} matches")
        
        for item in items[:5]:  # Check top 5
            if len(discoveries) >= max_discoveries:
                break
            
            repo = item['repository']['full_name']
            file_path = item['path']
            file_url = item['html_url']
            
            print(f"   📁 {repo}/{file_path}")
            
            # Get raw content
            raw_url = file_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            content_resp = requests.get(raw_url, headers=HEADERS, timeout=15)
            files_checked += 1
            
            if content_resp.status_code != 200:
                continue
            
            content = content_resp.text
            
            # Skip common false positives
            skip_keywords = ['example', 'placeholder', 'your_', 'test', 'sample', 'localhost', '127.0.0.1', 'fake', 'dummy', '***']
            if any(kw in content.lower() for kw in skip_keywords[:3]):
                print(f"      ⚠️ Skipping (appears to be example/test)")
                continue
            
            # Search for patterns
            found_secrets = []
            for pattern_name, pattern_regex in PATTERNS.items():
                matches = re.finditer(pattern_regex, content, re.MULTILINE)
                for match in matches:
                    secret = match.group(0)
                    # Additional validation
                    if len(secret) < 20:
                        continue
                    if 'example' in secret.lower() or 'test' in secret.lower():
                        continue
                    
                    found_secrets.append({
                        'type': pattern_name,
                        'secret': secret[:20] + '...',
                        'line': content[:match.start()].count('\n') + 1
                    })
            
            if found_secrets:
                discoveries.append({
                    'timestamp': datetime.now().isoformat(),
                    'repo': repo,
                    'file': file_path,
                    'url': file_url,
                    'search_target': target,
                    'secrets': found_secrets
                })
                print(f"   🚨 {len(found_secrets)} SECRET(S)!")
                for s in found_secrets:
                    print(f"      → {s['type']}: {s['secret']}")
                print(f"   💰 Total: {len(discoveries)}/{max_discoveries}")
    
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    
    print()

print("=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"Discoveries: {len(discoveries)}")
print(f"Files checked: {files_checked}")
print(f"Targets searched: {len(TARGETS)}")

if discoveries:
    report_file = f"reports/fresh_hunt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('reports', exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'discoveries': discoveries,
            'files_checked': files_checked
        }, f, indent=2)
    print(f"📄 Report: {report_file}")
    
    print("\n🎯 DISCOVERIES:")
    for d in discoveries:
        print(f"   {d['repo']}")
        print(f"   └── {len(d['secrets'])} secrets in {d['file']}")
else:
    print("\n😕 No live credentials found this run")
    print("   Try again later or expand targets")