#!/usr/bin/env python3
"""
Bulk Credential Hunter - Extended Discovery Mode

Runs continuous discovery without stopping on first hit.
Collects multiple credentials for responsible disclosure batch report.
"""

import os
import json
import base64
import requests
import re
import time
from datetime import datetime
from pathlib import Path

class BulkCredentialHunter:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.all_discoveries = []  # Collect ALL discoveries
        self.total_checked = 0
        self.rounds_completed = 0
        
        self.hunt_patterns = [
            {'query': 'mongodb+srv://username:password@cluster', 'name': 'MongoDB Atlas URI'},
            {'query': 'postgresql://user:pass@host.com', 'name': 'PostgreSQL URL'},
            {'query': 'JWT_SECRET=supersecrettoken', 'name': 'JWT Secret'},
            {'query': 'AKIAIOSFODNN7EXAMPLE', 'name': 'AWS Example (reverse)'},
            {'query': 'API_KEY=live_production_key', 'name': 'API Key in .env'},
            {'query': 'DATABASE_URL=postgres://user:pass', 'name': 'Database URL'},
            {'query': 'redis://:password@redis', 'name': 'Redis with Auth'},
            {'query': 'SECRET=production_secret_key', 'name': 'Secret in JSON'},
            {'query': 'key-mailgun-api-key32', 'name': 'Mailgun API Key'},
            {'query': 'ghp_productiontokentest', 'name': 'GitHub Classic PAT'},
            {'query': 'npm_productiontokentest', 'name': 'npm Token'},
            {'query': 'dckr_pat_dockertokentest', 'name': 'Docker PAT'},
            {'query': 'xoxb-slack-token-here', 'name': 'Slack Bot Token'},
        ]
    
    def search(self, query, per_page=10):
        url = "https://api.github.com/search/code"
        params = {'q': query, 'sort': 'indexed', 'order': 'desc', 'per_page': per_page}
        
        try:
            resp = self.session.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('items', []), data.get('total_count', 0)
            elif resp.status_code == 403:
                print(f"⏱️ Rate limited, waiting...")
                time.sleep(60)
                return [], 0
        except Exception as e:
            print(f"Search error: {e}")
        return [], 0
    
    def fetch_file(self, repo, path):
        for branch in ['main', 'master', 'develop', 'HEAD']:
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
    
    def extract_secrets(self, content, repo, path):
        findings = []
        
        patterns = [
            (r'mongodb(\+srv)?://[^:]+:([a-zA-Z0-9!@#$%^&*-_+=]{8,})@[^\s"\'`\)\]<>;]+', 'MongoDB Atlas URI', 1),
            (r'(postgres|mysql)://[^:]+:([^@]+)@[^\s"\'`\)\]<>;]+', 'Database URL', 1),
            (r'redis://:([a-zA-Z0-9!@#$%^&+=]{8,})@[^\s"\']+', 'Redis URL', 1),
            (r'["\']?(api[_-]?key|key)["\']?\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', 'API Key', 2),
            (r'["\']?jwt[_-]?secret["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{16,})["\']', 'JWT Secret', 1),
            (r'["\']?secret[_-]?key["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{16,})["\']', 'Secret Key', 1),
            (r'["\']?password["\']?\s*[=:]\s*["\']([a-zA-Z0-9!@#$%^&*-_+=]{8,})["\']', 'Password', 1),
            (r'ghp_[a-zA-Z0-9_]{36}', 'GitHub PAT', 0),
            (r'dckr_pat_[a-zA-Z0-9_-]{20,}', 'Docker PAT', 0),
            (r'npm_[a-zA-Z0-9]{36}', 'npm Token', 0),
        ]
        
        lines = content.split('\n')
        
        for pattern, name, group_num in patterns:
            for i, line in enumerate(lines):
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    if group_num > 0 and len(match.groups()) >= group_num:
                        secret_val = match.group(group_num)
                    else:
                        secret_val = match.group(0)
                    
                    if len(secret_val) < 8:
                        continue
                    
                    placeholders = ['example', 'your', 'replace', 'changeme', 'xxx', 'yyy', 
                                     'password', 'secret', 'test', 'fake', 'demo', 'sample',
                                     'insert', 'placeholder', 'none', 'null', 'process.env', 
                                     'env.', '${', 'getenv', 'config']
                    
                    if any(p in secret_val.lower() for p in placeholders):
                        continue
                    
                    if secret_val == secret_val.upper() and '=' in line and len(secret_val) < 20:
                        continue
                    
                    redacted = secret_val[:6] + "***" + secret_val[-4:] if len(secret_val) > 10 else "***" + secret_val[-4:]
                    
                    findings.append({
                        'type': name,
                        'line': i + 1,
                        'redacted': redacted,
                        'length': len(secret_val),
                        'snippet': line.strip()[:80]
                    })
        
        return findings
    
    def is_example_repo(self, repo):
        examples = ['example', 'demo', 'tutorial', 'template', 'starter', 
                   'boilerplate', 'sample', 'practice', 'lesson', 'test']
        return any(x in repo.lower() for x in examples)
    
    def save_progress(self):
        Path("reports").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = {
            'hunt_session': 'Bulk Discovery',
            'timestamp': timestamp,
            'rounds_completed': self.rounds_completed,
            'files_checked': self.total_checked,
            'discoveries_count': len(self.all_discoveries),
            'discoveries': self.all_discoveries
        }
        
        with open(f"reports/bulk_discovery_{timestamp}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save running log
        with open("reports/bulk_discovery_running.json", 'w') as f:
            json.dump(report, f, indent=2)
    
    def hunt(self, max_discoveries=5, max_rounds=150):
        print("🎯" * 35)
        print("   BULK CREDENTIAL HUNTER")
        print(f"   Target: {max_discoveries} discoveries")
        print(f"   Max rounds: {max_rounds}")
        print("🎯" * 35)
        print(f"\n🔫 Loaded {len(self.hunt_patterns)} patterns")
        
        pattern_idx = 0
        
        while len(self.all_discoveries) < max_discoveries and self.rounds_completed < max_rounds:
            pattern = self.hunt_patterns[pattern_idx % len(self.hunt_patterns)]
            self.rounds_completed += 1
            
            print(f"\n🔍 Round {self.rounds_completed}/{max_rounds} | Pattern: {pattern['name']}")
            print(f"   Target: {max_discoveries - len(self.all_discoveries)} more discoveries needed")
            
            items, total = self.search(pattern['query'], per_page=8)
            
            if total > 0:
                print(f"   Matches: {total}")
            
            if not items:
                time.sleep(2)
                pattern_idx += 1
                continue
            
            for item in items[:5]:
                repo = item['repository']['full_name']
                path = item['path']
                
                if self.is_example_repo(repo):
                    continue
                
                print(f"   📁 {repo[:40]}")
                
                content = self.fetch_file(repo, path)
                self.total_checked += 1
                
                if not content:
                    continue
                
                secrets = self.extract_secrets(content, repo, path)
                
                if secrets:
                    print(f"   🚨 {len(secrets)} SECRET(S)!")
                    for s in secrets[:3]:
                        print(f"      → {s['type']}: {s['redacted']}")
                    
                    discovery = {
                        'timestamp': datetime.now().isoformat(),
                        'pattern': pattern['name'],
                        'repo': repo,
                        'file': path,
                        'url': f"https://github.com/{repo}/blob/main/{path}",
                        'secrets': secrets,
                        'secret_count': len(secrets)
                    }
                    
                    self.all_discoveries.append(discovery)
                    self.save_progress()
                    
                    print(f"\n   💰 Total discoveries: {len(self.all_discoveries)}/{max_discoveries}")
                    
                    if len(self.all_discoveries) >= max_discoveries:
                        print(f"\n🎉 TARGET REACHED: {max_discoveries} discoveries!")
                        return True
            
            time.sleep(4)  # Rate limit
            pattern_idx += 1
            
            # Progress save every 10 rounds
            if self.rounds_completed % 10 == 0:
                print(f"\n📊 Progress: {len(self.all_discoveries)} discoveries")
        
        print(f"\n✅ Hunt complete: {len(self.all_discoveries)} discoveries in {self.rounds_completed} rounds")
        return len(self.all_discoveries) > 0

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT")
        exit(1)
    
    hunter = BulkCredentialHunter()
    hunter.hunt(max_discoveries=5, max_rounds=150)
    hunter.save_progress()
    
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total discoveries: {len(hunter.all_discoveries)}")
    print(f"Rounds completed: {hunter.rounds_completed}")
    print(f"Files checked: {hunter.total_checked}")
    print(f"\n📄 Report: reports/bulk_discovery_running.json")
