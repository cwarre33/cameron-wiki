#!/usr/bin/env python3
"""
Fresh Credential Hunter v2 - New Targets
Focus: API keys, tokens, secrets in recent commits
"""

import requests
import re
import json
import os
from datetime import datetime
from urllib.parse import quote

GITHUB_PAT = os.environ.get('GITHUB_PAT')
if not GITHUB_PAT:
    print("❌ Set GITHUB_PAT")
    exit(1)

HEADERS = {
    'Authorization': f'token {GITHUB_PAT}',
    'Accept': 'application/vnd.github.v3+json'
}

# NEW TARGETS - different patterns
TARGETS = [
    # API Keys
    "api_key created:>2025-01-01",
    "apikey created:>2025-01-01",
    "auth_token created:>2025-01-01",
    "access_token created:>2025-01-01",
    "bearer_token created:>2025-01-01",
    
    # Specific services
    "OPENAI_API_KEY created:>2025-04-01",
    "ANTHROPIC_API_KEY created:>2025-04-01",
    "GOOGLE_API_KEY created:>2025-04-01",
    "HF_TOKEN created:>2025-04-01",
    "GITHUB_TOKEN created:>2025-04-01",
    "AWS_SECRET_ACCESS_KEY created:>2025-04-01",
    
    # Config files with real data
    "filename:.env.production",
    "filename:secrets.json", 
    "filename:credentials.xml",
    "filename:id_rsa",
    "filename:id_ed25519",
]

# Refined patterns (production credentials only)
PATTERNS = {
    'OpenAI Key': r'sk-[a-zA-Z0-9]{48}',
    'Anthropic Key': r'sk-ant-[a-zA-Z0-9]{32,}',
    'Google AI Key': r'AIza[0-9a-zA-Z_-]{35}',
    'Hugging Face': r'hf_[a-zA-Z0-9]{32,}',
    'GitHub Token': r'(ghp|github_pat)_[a-zA-Z0-9]{36,}',
    'Stripe Live': r'sk_live_[0-9a-zA-Z]{24,}',
    'AWS Secret': r'[0-9a-zA-Z/+]{40}',
    'Private Key': r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
}

discoveries = []
files_checked = 0
max_discoveries = 5

print("=" * 60)
print("   FRESH CREDENTIAL HUNTER v2")
print("   New Patterns: API Keys & Tokens")
print("=" * 60)
print()

for target in TARGETS:
    if len(discoveries) >= max_discoveries:
        break
    
    print(f"🔍 Searching: {target[:50]}...")
    url = f"https://api.github.com/search/code?q={quote(target)}&sort=indexed&order=desc&per_page=10"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            if resp.status_code == 403:
                print(f"   ⚠️ Rate limited")
            else:
                print(f"   ⚠️ API error: {resp.status_code}")
            continue
        
        data = resp.json()
        items = data.get('items', [])
        print(f"   Found {len(items)} matches")
        
        for item in items[:3]:  # Check top 3 to avoid rate limits
            if len(discoveries) >= max_discoveries:
                break
            
            repo = item['repository']['full_name']
            file_path = item['path']
            file_url = item['html_url']
            
            print(f"   📁 {repo}/{file_path}")
            
            # Get raw content
            raw_url = file_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            try:
                content_resp = requests.get(raw_url, headers=HEADERS, timeout=10)
                files_checked += 1
            except:
                continue
            
            if content_resp.status_code != 200:
                continue
            
            content = content_resp.text
            
            # Skip examples/placeholders
            skip_keywords = ['example', 'placeholder', 'your_', 'test', 'sample', 'localhost', 
                           '127.0.0.1', 'fake', 'dummy', '***', 'xxxx', 'TODO', 'changeme']
            content_lower = content.lower()
            if sum(kw in content_lower for kw in skip_keywords) >= 2:
                print(f"      ⚠️ Skipping (examples/tests detected)")
                continue
            
            # Search for patterns
            found_secrets = []
            for pattern_name, pattern_regex in PATTERNS.items():
                matches = re.finditer(pattern_regex, content, re.MULTILINE)
                for match in matches:
                    secret = match.group(0)
                    if len(secret) < 20:
                        continue
                    
                    # Additional filtering
                    if any(bad in secret.lower() for bad in ['example', 'test', 'fake']):
                        continue
                    
                    found_secrets.append({
                        'type': pattern_name,
                        'secret': secret[:15] + '...',
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
                print(f"   🚨 {len(found_secrets)} POTENTIAL SECRET(S)!")
                for s in found_secrets[:3]:  # Show first 3
                    print(f"      → {s['type']}: {s['secret']}")
                print(f"   💰 Total: {len(discoveries)}/{max_discoveries}")
    
    except Exception as e:
        print(f"   ⚠️ Error: {str(e)[:50]}")
    
    print()

# Results
print("=" * 60)
print("HUNT COMPLETE")
print("=" * 60)
print(f"Discoveries: {len(discoveries)}")
print(f"Files checked: {files_checked}")
print(f"Targets searched: {len(TARGETS)}")

if discoveries:
    report_file = f"reports/hunt2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('reports', exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'discoveries': discoveries,
            'files_checked': files_checked
        }, f, indent=2)
    print(f"📄 Report: {report_file}")
    
    print("\n🎯 DISCOVERIES:")
    for i, d in enumerate(discoveries, 1):
        print(f"\n{i}. {d['repo']}")
        print(f"   └── {len(d['secrets'])} potential secrets in {d['file']}")
else:
    print("\n😕 No new discoveries this run")
    print("   Rate limits may have kicked in")

print("\n" + "=" * 60)