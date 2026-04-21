#!/usr/bin/env python3
"""
WOW Recon - Raw File API Approach

Pull exposed config files directly via GitHub API
No cloning needed - just grab the secrets
"""

import os
import json
import base64
import requests
from datetime import datetime
from pathlib import Path

class RawFileRecon:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.discoveries = []
        self.secrets_found = 0
        
    def search_targets(self, query, max_items=15):
        """Search for files matching pattern"""
        url = "https://api.github.com/search/code"
        params = {'q': query, 'sort': 'indexed', 'order': 'desc', 'per_page': max_items}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json().get('items', [])
        except Exception as e:
            print(f"  Search error: {e}")
        return []
    
    def fetch_file_content(self, repo_full_name, file_path, ref='main'):
        """Fetch raw file content via API"""
        # Try several common branches
        branches = [ref, 'master', 'main', 'develop', 'dev']
        
        for branch in branches:
            url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}?ref={branch}"
            try:
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    content = base64.b64decode(data.get('content', '')).decode('utf-8', errors='ignore')
                    return content, branch
            except Exception:
                continue
        return None, None
    
    def extract_secrets(self, content, repo_name, file_path, source):
        """Scan content for credential patterns"""
        findings = []
        lines = content.split('\n')
        
        # High-impact patterns
        patterns = {
            'MongoDB URI': r'mongodb\+srv://[^:]+:[^@]+@',
            'AWS Key': r'AKIA[0-9A-Z]{16}',
            'AWS Secret': r'aws_secret_access_key[:\s=]+["\']?([A-Za-z0-9/+=]{40})["\']?',
            'OpenAI Key': r'sk-[a-zA-Z0-9]{48}',
            'Slack Token': r'xox[baprs]-[0-9]+-[0-9]+-[a-zA-Z0-9]+',
            'Stripe Live': r'sk_live_[a-zA-Z0-9]{24,}',
            'Generic JWT': r'jwt_secret[:\s=]+["\']?([a-zA-Z0-9_-]+)["\']?',
            'Private Key': r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
            'Database URL': r'database[_\s]?url[:\s=]+["\']?([^"\']+\+srv://[^"\']+)',
            'Firebase': r'firebase.*api[_\s]?key[:\s=]+["\']?([a-zA-Z0-9_-]+)',
            'Password': r'password[:\s=]+["\']?([^"\']{8,})["\']?',
            'Secret Key': r'secret[_\s]?key[:\s=]+["\']?([^"\']+)',
        }
        
        import re
        
        for pattern_name, pattern in patterns.items():
            for i, line in enumerate(lines):
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Redact actual secret for safety
                    redacted = str(match)[:10] + "***REDACTED" if len(str(match)) > 10 else "***REDACTED"
                    findings.append({
                        'pattern': pattern_name,
                        'line': i + 1,
                        'match': redacted,
                        'snippet': line[:80].strip(),
                    })
                    self.secrets_found += 1
        
        return findings
    
    def run_discovery(self):
        """Main discovery workflow"""
        print("🔥" * 35)
        print("      WOW RAW FILE DISCOVERY")
        print(f"      Started: {datetime.now().strftime('%H:%M:%S')}")
        print("🔥" * 35)
        print()
        
        # Define high-value search queries (URL-encoded versions)
        searches = [
            {'query': 'filename:.env.example', 'desc': '.env.example files'},
            {'query': 'filename:.env.development', 'desc': '.env.development files'},
            {'query': 'filename:.env.production', 'desc': '.env.production files'},
            {'query': 'filename:.env.local', 'desc': '.env.local files'},
            {'query': 'filename:config.json db_password', 'desc': 'Config with DB password'},
            {'query': 'filename:secrets.json', 'desc': 'Secrets.json files'},
            {'query': 'filename:credentials.json', 'desc': 'Credentials.json files'},
            {'query': 'filename:.aws credentials', 'desc': 'AWS credentials files'},
        ]
        
        all_targets = []
        
        for search in searches:
            print(f"🔍 {search['desc']}")
            items = self.search_targets(search['query'], max_items=12)
            
            for item in items:
                all_targets.append({
                    'repo': item['repository']['full_name'],
                    'repo_url': item['repository']['html_url'],
                    'file': item['path'],
                    'score': self._score_target(item['path']),
                })
        
        # Sort and deduplicate
        seen = set()
        unique = []
        for t in sorted(all_targets, key=lambda x: x['score'], reverse=True):
            key = f"{t['repo']}/{t['file']}"
            if key not in seen:
                seen.add(key)
                unique.append(t)
        
        print(f"\n🎯 Found {len(all_targets)} total files, {len(unique)} unique")
        print("=" * 55)
        
        # Scan top N files
        top_targets = unique[:10]
        
        for target in top_targets:
            repo = target['repo']
            file_path = target['file']
            
            # Skip test/lecture/example repos
            if any(x in repo.lower() for x in ['tutorial', 'example', 'test', 'demo', 'course', 'lesson', 'practice', 'starter']):
                continue
            
            print(f"\n📄 {repo}/{file_path}")
            
            content, branch = self.fetch_file_content(repo, file_path)
            
            if content:
                secrets = self.extract_secrets(content, repo, file_path, 'api')
                
                if secrets:
                    print(f"   🚨 FOUND {len(secrets)} SECRET(S)!")
                    for s in secrets[:5]:  # Show top 5
                        print(f"      → {s['pattern']} (line {s['line']})")
                        print(f"        {s['snippet'][:60]}...")
                    
                    self.discoveries.append({
                        'repo': repo,
                        'file': file_path,
                        'url': f"https://github.com/{repo}/blob/{branch}/{file_path}",
                        'secrets': secrets,
                        'found_at': datetime.now().isoformat()
                    })
                else:
                    print(f"   ✅ No high-value secrets detected")
            else:
                print(f"   ⚠️  Could not fetch file")
        
        self._save_report()
    
    def _score_target(self, file_path):
        """Score the likelihood of finding live secrets"""
        score = 0
        fp = file_path.lower()
        
        # Production files are highest value
        if 'prod' in fp or 'production' in fp: score += 15
        if 'dev' in fp and 'prod' not in fp: score += 5
        if 'example' in fp: score -= 5  # Probably fake/example data
        if 'test' in fp: score -= 3
        
        # File types
        if '.env' in fp: score += 10
        if 'secret' in fp: score += 12
        if 'cred' in fp: score += 10
        if 'aws' in fp: score += 8
        if 'config' in fp: score += 5
        
        return score
    
    def _save_report(self):
        """Save discovery report"""
        Path("reports").mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"reports/wow_rawfile_{timestamp}.json"
        
        report = {
            'session': 'WOW Raw File Discovery',
            'timestamp': datetime.now().isoformat(),
            'total_secrets_found': self.secrets_found,
            'files_with_secrets': len(self.discoveries),
            'discoveries': self.discoveries
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 55)
        print("DISCOVERY COMPLETE")
        print("=" * 55)
        print(f"Total secrets found: {self.secrets_found}")
        print(f"Files with secrets: {len(self.discoveries)}")
        print(f"\n📄 Report saved: {report_file}")
        
        if self.discoveries:
            print("\n🚨 TOP FINDINGS:")
            for d in self.discoveries[:3]:
                print(f"   • {d['repo']}: {len(d['secrets'])} secrets")

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT first")
        exit(1)
    
    recon = RawFileRecon()
    recon.run_discovery()
