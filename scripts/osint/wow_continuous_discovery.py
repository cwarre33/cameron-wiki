#!/usr/bin/env python3
"""
WOW Continuous Discovery Loop

Runs continuous discovery scanning across multiple patterns.
Loops through high-value credential patterns, saves all findings,
and reports discoveries in real-time.

Usage:
    export GITHUB_PAT="your_token"
    python3 scripts/osint/wow_continuous_discovery.py
"""

import os
import json
import base64
import requests
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ContinuousDiscovery:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.all_discoveries = []
        self.session_count = 0
        self.start_time = datetime.now()
        
        # High-value search patterns to loop through
        self.search_patterns = [
            {'query': 'AWS_ACCESS_KEY_ID="AKIA"', 'name': 'AWS Access Keys', 'priority': 10},
            {'query': 'DATABASE_URL="postgresql://"', 'name': 'PostgreSQL DB URLs', 'priority': 9},
            {'query': 'MONGODB_URI="mongodb+srv://"', 'name': 'MongoDB Atlas URIs', 'priority': 10},
            {'query': 'OPENAI_API_KEY="sk-', 'name': 'OpenAI API Keys', 'priority': 8},
            {'query': 'JWT_SECRET=" extension:env', 'name': 'JWT Secrets', 'priority': 7},
            {'query': 'STRIPE_SECRET_KEY="sk_live', 'name': 'Stripe Live Keys', 'priority': 10},
            {'query': 'SLACK_TOKEN="xoxb-', 'name': 'Slack Bot Tokens', 'priority': 8},
            {'query': 'FIREBASE_API_KEY="AIza', 'name': 'Firebase API Keys', 'priority': 7},
            {'query': 'GITHUB_TOKEN="ghp_', 'name': 'GitHub PATs', 'priority': 9},
            {'query': 'SENDGRID_API_KEY="SG.', 'name': 'SendGrid Keys', 'priority': 8},
            {'query': 'REDIS_URL="redis://"', 'name': 'Redis URLs', 'priority': 6},
            {'query': 'AUTH0_CLIENT_SECRET="', 'name': 'Auth0 Secrets', 'priority': 7},
            {'query': 'GOOGLE_CLIENT_SECRET="', 'name': 'Google OAuth', 'priority': 7},
            {'query': 'MYSQL_PASSWORD="', 'name': 'MySQL Passwords', 'priority': 6},
            {'query': 'PRIVATE_KEY="-----BEGIN', 'name': 'Private Keys', 'priority': 10},
        ]
        
        self.current_pattern_index = 0
    
    def check_rate_limit(self):
        """Check GitHub API rate limits"""
        try:
            resp = self.session.get('https://api.github.com/rate_limit', timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                core = data['resources']['core']
                search = data['resources']['search']
                return {
                    'core_remaining': core['remaining'],
                    'core_limit': core['limit'],
                    'core_reset': core['reset'],
                    'search_remaining': search['remaining'],
                    'search_limit': search['limit'],
                    'search_reset': search['reset']
                }
        except Exception as e:
            print(f"Rate check error: {e}")
        return None
    
    def search_code(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search GitHub code"""
        url = "https://api.github.com/search/code"
        params = {
            'q': query,
            'sort': 'indexed',
            'order': 'desc',
            'per_page': per_page
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=20)
            if resp.status_code == 200:
                return resp.json().get('items', [])
            elif resp.status_code == 403:
                print(f"⚠️ Rate limited on search")
                return []
        except Exception as e:
            print(f"Search error: {e}")
        return []
    
    def fetch_file_content(self, repo: str, path: str) -> str:
        """Fetch raw file content from repo"""
        branches = ['main', 'master', 'develop', 'dev']
        
        for branch in branches:
            url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('content'):
                        return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            except:
                continue
        return None
    
    def extract_secrets(self, content: str) -> List[Dict]:
        """Extract actual secrets from file content"""
        findings = []
        
        patterns = [
            (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
            (r'AIza[0-9A-Za-z_-]{35}', 'Firebase API Key'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'[A-Za-z0-9/+=]{40}', 'AWS Secret Key'),  # Generic 40-char (context needed)
            (r'xox[baprs]-[0-9]+-[0-9]+-[a-zA-Z0-9]+', 'Slack Token'),
            (r'sk_(live|test)_[a-zA-Z0-9]{24,}', 'Stripe Key'),
            (r'ghp_[A-Za-z0-9_]{36}', 'GitHub PAT'),
            (r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}', 'SendGrid Key'),
            (r'[a-f0-9]{32}-us[0-9]{1,2}', 'Mailchimp Key'),
            (r'private[_-\s]?key[:\s]*["\']?([^"\']{20,})', 'Private Key'),
        ]
        
        lines = content.split('\n')
        
        for pattern_name, pattern in patterns:
            for i, line in enumerate(lines):
                matches = re.finditer(pattern, line)
                for match in matches:
                    match_text = match.group(0)
                    
                    # Skip placeholders
                    placeholders = ['example', 'fake', 'test', 'dummy', 'change',
                                  'your', 'replace', 'xxx', 'yyy', 'zzz', '${',
                                  'process.env', 'env.', 'import', 'const', 'let']
                    if any(p in match_text.lower() for p in placeholders):
                        continue
                    
                    # Skip if too short
                    if len(match_text) < 10:
                        continue
                    
                    # Redact for safety
                    redacted = match_text[:10] + "***REDACTED***" + match_text[-4:] if len(match_text) > 14 else "***REDACTED***"
                    
                    findings.append({
                        'type': pattern_name,
                        'line': i + 1,
                        'match': redacted,
                        'context': line.strip()[:80]
                    })
        
        return findings
    
    def is_example_file(self, repo: str, content: str) -> bool:
        """Check if file is example/template rather than real config"""
        repo_lower = repo.lower()
        content_lower = content.lower()
        
        # Check repo name
        if any(x in repo_lower for x in ['example', 'demo', 'tutorial', 'template', 'starter', 'sample', 'boilerplate']):
            return True
        
        # Check content
        if any(x in content_lower for x in ['your_', 'replace_me', 'example.com', 'changeme']):
            return True
        
        return False
    
    def save_discovery(self, discovery: Dict):
        """Save discovery to file"""
        Path("reports".format()).mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with open(f"reports/discovery_{timestamp}.json", 'w') as f:
            json.dump(discovery, f, indent=2)
        
        self.all_discoveries.append(discovery)
        
        # Also append to master log
        with open("reports/discovery_log.jsonl", 'a') as f:
            json.dump({**discovery, 'timestamp': timestamp}, f)
            f.write('\n')
    
    def print_stats(self):
        """Print current session stats"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.session_count / (elapsed / 60) if elapsed > 0 else 0
        
        print(f"\n📊 SESSION STATS")
        print(f"   Runtime: {elapsed/60:.1f} minutes")
        print(f"   Patterns searched: {self.session_count}/{len(self.search_patterns)}")
        print(f"   Total discoveries: {len(self.all_discoveries)}")
        print(f"   Rate: {rate:.1f} patterns/minute")
        print()
    
    def run_discovery_round(self):
        """Run one discovery round"""
        pattern = self.search_patterns[self.current_pattern_index]
        
        print(f"\n🔍 ROUND {self.session_count + 1}: {pattern['name']}")
        print(f"   Query: {pattern['query'][:50]}...")
        print(f"   Priority: {pattern['priority']}/10")
        
        # Check rate limits
        rate_status = self.check_rate_limit()
        if rate_status:
            if rate_status['search_remaining'] < 5:
                reset_time = datetime.fromtimestamp(rate_status['search_reset'])
                wait_seconds = (reset_time - datetime.now()).total_seconds()
                if wait_seconds > 0:
                    print(f"⏱️ Search limit hit. Waiting {wait_seconds/60:.0f} minutes...")
                    time.sleep(min(wait_seconds, 300))  # Wait max 5 minutes
            else:
                print(f"   Rate: {rate_status['search_remaining']}/{rate_status['search_limit']} searches remaining")
        
        # Search
        items = self.search_code(pattern['query'], per_page=8)
        print(f"   Found: {len(items)} files")
        
        discoveries_in_round = 0
        
        for item in items[:5]:  # Top 5 from each pattern
            repo = item['repository']['full_name']
            path = item['path']
            html_url = item['html_url']
            
            print(f"   📄 {repo}: {path[:40]}")
            
            # Fetch content
            content = self.fetch_file_content(repo, path)
            
            if content:
                # Check if it's just an example
                if self.is_example_file(repo, content):
                    print(f"      ⚪ Example file - skipped")
                    continue
                
                # Extract secrets
                secrets = self.extract_secrets(content)
                
                if secrets:
                    discoveries_in_round += 1
                    print(f"      🔥 {len(secrets)} SECRET(S) FOUND!")
                    for s in secrets[:3]:
                        print(f"         → {s['type']}: {s['match']}")
                    
                    self.save_discovery({
                        'pattern': pattern['name'],
                        'repo': repo,
                        'path': path,
                        'url': html_url,
                        'secrets': secrets
                    })
                else:
                    print(f"      ✅ File fetched, no high-value secrets")
            else:
                print(f"      ⚠️ Could not fetch content")
        
        self.session_count += 1
        self.current_pattern_index = (self.current_pattern_index + 1) % len(self.search_patterns)
        
        print(f"   Round complete. {discoveries_in_round} discoveries this round.")
        
        # Rate limiting delay
        time.sleep(6)  # 10 searches/minute max
    
    def run_continuous(self, rounds: int = 0):
        """Run continuous discovery
        
        Args:
            rounds: Number of rounds (0 = infinite)
        """
        print("🌟" * 35)
        print("   WOW CONTINUOUS DISCOVERY")
        print("   Running until interrupted...")
        print("   Press Ctrl+C to stop")
        print("🌟" * 35)
        print(f"\n📋 Loaded {len(self.search_patterns)} search patterns")
        print(f"🎯 Targeting: {len(self.search_patterns)} pattern categories")
        
        try:
            round_num = 0
            while True:
                if rounds > 0 and round_num >= rounds:
                    print(f"\n✅ Completed {rounds} rounds")
                    break
                
                self.run_discovery_round()
                round_num += 1
                
                # Print stats every 5 rounds
                if round_num % 5 == 0:
                    self.print_stats()
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        finally:
            self.print_stats()
            print(f"\n💾 {len(self.all_discoveries)} total discoveries saved")
            print("📝 Reports in: reports/")

if __name__ == '__main__':
    import sys
    
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Please set GITHUB_PAT environment variable")
        print("   export GITHUB_PAT='your_github_pat'")
        sys.exit(1)
    
    # Parse rounds from args
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    discovery = ContinuousDiscovery()
    discovery.run_continuous(rounds=rounds)
