#!/usr/bin/env python3
"""
AGGRESSIVE Live Credential Hunter

Targets actual exposed secrets (not env var names).
Searches for real API keys, passwords, tokens, URIs with embedded creds.
"""

import os
import json
import base64
import requests
import re
import time
from datetime import datetime
from pathlib import Path

class LiveCredentialHunter:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.live_secrets = []
        self.total_checked = 0
        
        # Patterns that find ACTUAL credential values
        self.hunt_patterns = [
            # MongoDB Atlas URIs with real passwords
            {'query': 'mongodb+srv://[a-z]+:[a-zA-Z0-9]+@cluster', 'name': 'MongoDB Atlas URI'},
            # PostgreSQL URLs with real creds
            {'query': 'postgresql://[a-z]+:[^@]+@[a-z]+.com', 'name': 'PostgreSQL URL'},
            # JWT secrets that look real
            {'query': 'JWT_SECRET=[a-zA-Z0-9]{20,}', 'name': 'JWT Secret'},
            # AWS keys
            {'query': 'AKIAIOSFODNN7EXAMPLE', 'name': 'AWS Example (reverse hunt)'},
            # Generic: filename:.env with API keys
            {'query': 'API_KEY=[a-zA-Z0-9_-]{20,} filename:.env', 'name': 'API Key in .env'},
            # Generic: DATABASE_URL with actual protocol
            {'query': 'DATABASE_URL=[a-z]+:// username', 'name': 'Database URL'},
            # Redis with auth
            {'query': 'redis://:[a-zA-Z0-9]+@redis', 'name': 'Redis with Auth'},
            # Generic secrets in configs
            {'query': 'SECRET=[a-zA-Z0-9_]{16,} extension:json', 'name': 'Secret in JSON'},
            # Mailgun, SendGrid tokens
            {'query': 'key-[a-f0-9]{32}', 'name': 'Mailgun API Key'},
            # GitHub tokens (classic)
            {'query': 'ghp_[a-zA-Z0-9_]{36}', 'name': 'GitHub Classic PAT'},
            # npm tokens
            {'query': 'npm_[a-zA-Z0-9]{36}', 'name': 'npm Token'},
            # Docker registry tokens
            {'query': 'dckr_pat_[a-zA-Z0-9_-]{20,}', 'name': 'Docker PAT'},
            # Slack tokens with different prefixes
            {'query': 'xoxb-[0-9]{10,12}-[0-9]{10,12}', 'name': 'Slack Bot Token'},
        ]
    
    def search(self, query, per_page=10):
        """Search GitHub code"""
        url = "https://api.github.com/search/code"
        params = {'q': query, 'sort': 'indexed', 'order': 'desc', 'per_page': per_page}
        
        try:
            resp = self.session.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('items', []), data.get('total_count', 0)
            elif resp.status_code == 403:
                print(f"⏱️ Rate limited")
                return [], 0
        except Exception as e:
            print(f"Search error: {e}")
        return [], 0
    
    def fetch_file(self, repo, path):
        """Fetch file content"""
        for branch in ['main', 'master', 'develop', 'dev', 'HEAD']:
            url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    if 'content' in data:
                        return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            except:
                continue
        return None
    
    def extract_real_secrets(self, content, repo, path):
        """Extract ONLY actual credential values"""
        findings = []
        
        # High-confidence patterns for real secrets
        real_patterns = [
            # MongoDB Atlas with password
            (r'mongodb(\+srv)?://[^:]+:([a-zA-Z0-9!@#$%^&*-_+=]{8,})@[^\s"\'`\)\]<>;]+', 'MongoDB Atlas URI'),
            # PostgreSQL/MySQL with password
            (r'(postgres|mysql)://[^:]+:([^@]+)@[^\s"\'`\)\]<>;]+', 'Database URL'),
            # Redis with password
            (r'redis://:([a-zA-Z0-9!@#$%^&+=]{8,})@[^\s"\']+', 'Redis URL'),
            # API keys (min 20 chars, looks random)
            (r'["\']?(api[_-]?key|key)["\']?\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', 'API Key'),
            # JWT secrets (long random strings)
            (r'["\']?jwt[_-]?secret["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{16,})["\']', 'JWT Secret'),
            # Secret keys
            (r'["\']?secret[_-]?key["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{16,})["\']', 'Secret Key'),
            # General password (not placeholder)
            (r'["\']?password["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{8,})["\']', 'Password'),
            # GitHub tokens
            (r'ghp_[a-zA-Z0-9_]{36}', 'GitHub PAT'),
            # Docker tokens
            (r'dckr_pat_[a-zA-Z0-9_-]{20,}', 'Docker PAT'),
        ]
        
        lines = content.split('\n')
        
        for pattern, name in real_patterns:
            for i, line in enumerate(lines):
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Get the actual secret value (usually group 1 or full match)
                    if match.groups():
                        secret_val = match.group(1) or match.group(0)
                    else:
                        secret_val = match.group(0)
                    
                    # Skip if too short or looks like placeholder
                    if len(secret_val) < 8:
                        continue
                    
                    placeholder_indicators = ['example', 'your', 'replace', 'changeme', 'xxx', 'yyy', 
                                               'password', 'secret', 'test', 'fake', 'demo', 'sample',
                                               'insert', 'placeholder', 'none', 'null', 'undefined',
                                               'process.env', 'env.', '${', 'getenv', 'config']
                    
                    if any(p in secret_val.lower() for p in placeholder_indicators):
                        continue
                    
                    # Skip if it's a variable name not value
                    if secret_val == secret_val.upper() and '=' in line:
                        continue
                    
                    # It's a live secret!
                    redacted = secret_val[:6] + "***" + secret_val[-4:] if len(secret_val) > 10 else "***REDACTED***"
                    
                    findings.append({
                        'type': name,
                        'line': i + 1,
                        'value_redacted': redacted,
                        'length': len(secret_val),
                        'context': line.strip()[:60]
                    })
        
        return findings
    
    def is_example_repo(self, repo):
        """Check if repo is likely an example/template"""
        example_indicators = ['example', 'demo', 'tutorial', 'template', 'starter', 
                             'boilerplate', 'sample', 'practice', 'lesson', 'course',
                             'learn', 'how-to', 'getting-started', 'hello-world',
                             'test', 'mock', 'dummy', 'fake']
        return any(x in repo.lower() for x in example_indicators)
    
    def hunt(self):
        """Main hunt loop"""
        print("🎯" * 35)
        print("   LIVE CREDENTIAL HUNTER")
        print("   Finding actual secrets...")
        print("🎯" * 35)
        print(f"\n🔫 Loaded {len(self.hunt_patterns)} high-yield patterns")
        
        round_num = 0
        
        while True:
            for pattern in self.hunt_patterns:
                round_num += 1
                print(f"\n🔍 ROUND {round_num}: {pattern['name']}")
                print(f"   Query: {pattern['query'][:50]}...")
                
                # Search
                items, total = self.search(pattern['query'], per_page=8)
                print(f"   GitHub says: {total} matches")
                
                if not items:
                    time.sleep(2)
                    continue
                
                # Check each result
                checked_this_round = 0
                for item in items[:5]:  # Top 5
                    repo = item['repository']['full_name']
                    path = item['path']
                    
                    # Skip examples
                    if self.is_example_repo(repo):
                        continue
                    
                    print(f"   📁 {repo[:40]}/{path[:30]}")
                    
                    # Fetch content
                    content = self.fetch_file(repo, path)
                    self.total_checked += 1
                    checked_this_round += 1
                    
                    if not content:
                        print(f"      ⚠️ Could not fetch")
                        continue
                    
                    # Extract secrets
                    secrets = self.extract_real_secrets(content, repo, path)
                    
                    if secrets:
                        print(f"   🚨🚨🚨 LIVE SECRETS FOUND! 🚨🚨🚨")
                        print(f"      Repository: {repo}")
                        print(f"      File: {path}")
                        print(f"      Count: {len(secrets)}")
                        print(f"      Secrets:")
                        for s in secrets[:5]:
                            print(f"        → {s['type']}: {s['value_redacted']} (len {s['length']})")
                        
                        discovery = {
                            'timestamp': datetime.now().isoformat(),
                            'pattern': pattern['name'],
                            'repo': repo,
                            'file': path,
                            'url': f"https://github.com/{repo}/blob/main/{path}",
                            'secrets': secrets,
                            'total_secrets': len(secrets)
                        }
                        
                        self.live_secrets.append(discovery)
                        self.save_discovery(discovery)
                        
                        # HUGE WIN - print summary
                        print(f"\n{'='*60}")
                        print("💀💀💀 LIVE CREDENTIAL DISCOVERED 💀💀💀")
                        print(f"{'='*60}")
                        print(f"Total discoveries: {len(self.live_secrets)}")
                        print(f"Files checked: {self.total_checked}")
                        
                        return True  # Stop on first discovery
                    else:
                        print(f"      ✅ Clean")
                
                print(f"   Round complete. Checked {checked_this_round} files.")
                
                # Rate limit
                time.sleep(6)
                
                # Stats every 10 rounds
                if round_num % 10 == 0:
                    self.print_stats(round_num)
        
        return False
    
    def save_discovery(self, discovery):
        """Save discovery to file"""
        Path("reports").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with open(f"reports/LIVE_CREDENTIAL_{timestamp}.json", 'w') as f:
            json.dump(discovery, f, indent=2)
        
        # Also append to master
        with open("reports/live_credentials_log.jsonl", 'a') as f:
            f.write(json.dumps(discovery) + '\n')
    
    def print_stats(self, round_num):
        """Print current stats"""
        print(f"\n{'='*60}")
        print(f"STATS (Round {round_num})")
        print(f"Files checked: {self.total_checked}")
        print(f"Live secrets found: {len(self.live_secrets)}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT first")
        exit(1)
    
    hunter = LiveCredentialHunter()
    try:
        found = hunter.hunt()
        if found:
            print("\n✅ Hunting complete - live credentials found!")
        else:
            print("\n⚪ No live credentials in this session")
    except KeyboardInterrupt:
        print(f"\n\n🛑 Stopped by user")
        print(f"Checked {hunter.total_checked} files")
        print(f"Found {len(hunter.live_secrets)} live secrets")
