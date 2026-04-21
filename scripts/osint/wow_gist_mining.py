#!/usr/bin/env python3
"""
WOW Recon - Gist Mining

Gists are the HIGHEST-YIELD surface for secrets:
- Created quickly, often forgotten
- Used for sharing sensitive configs temporarily
- Not as well monitored as repos
- Full content searchable via API
"""

import os
import json
import base64
import requests
import re
from datetime import datetime
from pathlib import Path

class GistRecon:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.discoveries = []
        self.secrets_found = 0
        
    def search_gists(self, query, max_items=15):
        """Search public gists for code matching query"""
        url = "https://api.github.com/gists"
        
        # We can't directly search gists, so we'll use the public timeline
        # and filter, OR get user gists
        # Better approach: use search endpoint with q param if available
        
        # Try the gist search via code search
        search_url = "https://api.github.com/search/code"
        params = {
            'q': f'{query} extension:json',  # Search code in gists
            'sort': 'indexed',
            'order': 'desc',
        }
        
        try:
            response = self.session.get(search_url, params=params, timeout=20)
            if response.status_code == 200:
                items = response.json().get('items', [])
                # Filter to only items where repository has type 'gist'
                gist_items = [i for i in items if 'gist.github.com' in i.get('html_url', '')]
                return gist_items[:max_items]
        except Exception as e:
            print(f"  Search error: {e}")
        return []
    
    def fetch_gist_content(self, gist_id):
        """Fetch raw content of a gist"""
        url = f"https://api.github.com/gists/{gist_id}"
        
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None
    
    def extract_secrets(self, content, gist_id, filename):
        """Extract credential patterns from gist content"""
        findings = []
        
        # Comprehensive patterns
        patterns = [
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'["\']?AWS_SECRET_ACCESS_KEY["\']?\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})', 'AWS Secret Key'),
            (r'mongodb(\+srv)?://[^:]+:([^@]+)@[^\s"]+', 'MongoDB URI'),
            (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
            (r'(postgres|mysql|redis)://[^:]+:[^@]+@[^\s"]+', 'Database URL'),
            (r'sk_(live|test)_[a-zA-Z0-9]{24,}', 'Stripe Key'),
            (r'xox[baprs]-[0-9]+-[0-9]+-[a-zA-Z0-9]+', 'Slack Token'),
            (r'AIza[0-9A-Za-z_-]{35}', 'Firebase API Key'),
            (r'ghp_[A-Za-z0-9_]{36}', 'GitHub PAT'),
            (r'["\']?[Aa]pi[_-]?[Kk]ey["\']?\s*[=:]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?', 'Generic API Key'),
            (r'["\']?[Ss]ecret["\']?\s*[=:]\s*["\']([^"\']{12,})["\']?', 'Secret'),
            (r'["\']?[Pp]assword["\']?\s*[=:]\s*["\']([^"\']{8,})["\']?', 'Password'),
            (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'Private Key'),
            (r'pt_[a-zA-Z0-9]{20,}', 'Postman API Key'),
            (r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}', 'SendGrid API Key'),
        ]
        
        lines = content.split('\n')
        
        for pattern_name, pattern in patterns:
            for line in lines:
                for match in re.finditer(pattern, line):
                    match_text = match.group(0)
                    
                    # Skip obviously fake/test placeholders
                    if self._is_placeholder(match_text):
                        continue
                    
                    # Redact for safety
                    redacted = self._redact(match_text)
                    
                    findings.append({
                        'pattern': pattern_name,
                        'line_text': line.strip()[:100],
                        'redacted': redacted
                    })
                    self.secrets_found += 1
        
        return findings
    
    def _is_placeholder(self, text):
        """Check if value is a placeholder"""
        placeholders = ['example', 'fake', 'test', 'dummy', 'changeme',
                       'your_', 'my_', 'password', 'insert', 'placeholder',
                       'KEY_HERE', 'SECRET_HERE', 'xxx', 'YYY',
                       'replace', 'TODO', 'FIXME', 'none', 'undefined']
        return any(p in text.lower() for p in placeholders)
    
    def _redact(self, text):
        """Redact sensitive parts"""
        if len(text) < 15:
            return text[:4] + '***'
        return text[:10] + '***REDACTED***' + text[-4:]
    
    def run_discovery(self):
        """Main discovery workflow"""
        print("\n" + "💰" * 30)
        print("          GIST GOLD MINING")
        print("          Targeting forgotten snippets...")
        print(f"          Started: {datetime.now().strftime('%H:%M:%S')}")
        print("💰" * 30)
        print()
        
        # Alternative: search for code patterns that often appear in gists with secrets
        # Use code search with gist in URL
        searches = [
            {'pattern': 'mongodb+srv', 'desc': 'MongoDB connection strings'},
            {'pattern': 'sk_live', 'desc': 'Stripe live keys'},
            {'pattern': 'AKIA', 'desc': 'AWS access keys'},
            {'pattern': 'xoxb-', 'desc': 'Slack bot tokens'},
            {'pattern': 'jwt_secret', 'desc': 'JWT secrets'},
            {'pattern': 'OPENAI_API_KEY', 'desc': 'OpenAI keys'},
        ]
        
        all_items = []
        
        for search in searches:
            print(f"🔍 {search['desc']}")
            
            # Use code search with language:json to find config files
            url = "https://api.github.com/search/code"
            params = {
                'q': f"{search['pattern']} in:file",
                'sort': 'indexed',
                'order': 'desc',
                'per_page': 30
            }
            
            try:
                response = self.session.get(url, params=params, timeout=20)
                if response.status_code == 200:
                    items = response.json().get('items', [])
                    print(f"   Found: {len(items)} files")
                    all_items.extend(items)
            except Exception as e:
                print(f"   Error: {e}")
        
        # Deduplicate
        seen = set()
        unique_items = []
        for item in all_items:
            key = item['html_url']
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        
        print(f"\n🎯 {len(unique_items)} unique files to investigate")
        print("=" * 60)
        
        # Check top files
        for item in unique_items[:20]:
            file_path = item['path']
            html_url = item['html_url']
            
            # Skip obvious test/example repos
            if any(x in html_url.lower() for x in ['example', 'test', 'demo', 'tutorial', 'practice', 'lesson', '.test.']):
                continue
            
            print(f"\n📄 {file_path[:60]}")
            print(f"   URL: {html_url[:70]}...")
            
            # Extract repo info and fetch file
            repo_name = item['repository']['full_name']
            
            # Get file via API
            content, _ = self._fetch_raw_file(repo_name, file_path)
            
            if content:
                # Scan for secrets
                secrets = self.extract_secrets(content, 'search', file_path)
                
                if secrets:
                    print(f"   🚨 FOUND {len(secrets)} SECRET(S)!")
                    for s in secrets[:4]:
                        print(f"      → {s['pattern']}: {s['redacted']}")
                    
                    self.discoveries.append({
                        'file': file_path,
                        'repo': repo_name,
                        'url': html_url,
                        'secrets': secrets
                    })
                else:
                    print(f"   ✅ Clean")
            else:
                print(f"   ⚠️  Could not fetch")
        
        self._save_report()
    
    def _fetch_raw_file(self, repo, path):
        """Fetch raw file content"""
        branches = ['main', 'master', 'develop', 'dev']
        
        for branch in branches:
            url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
            try:
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('content'):
                        content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                        return content, branch
            except:
                continue
        
        # Try raw URL
        try:
            raw_url = f"https://raw.githubusercontent.com/{repo}/main/{path}"
            response = self.session.get(raw_url, timeout=10)
            if response.status_code == 200:
                return response.text, 'main'
        except:
            pass
        
        return None, None
    
    def _save_report(self):
        """Save report"""
        Path("reports").mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"reports/wow_gist_mining_{timestamp}.json"
        
        report = {
            'session': 'WOW Gist Mining',
            'timestamp': datetime.now().isoformat(),
            'total_secrets_found': self.secrets_found,
            'files_with_secrets': len(self.discoveries),
            'discoveries': self.discoveries
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 60)
        print("GIST MINING COMPLETE")
        print("=" * 60)
        print(f"Total secrets found: {self.secrets_found}")
        print(f"Files with secrets: {len(self.discoveries)}")
        
        if self.discoveries:
            print("\n🔥🚨🔥 TOP DISCOVERIES:")
            for d in self.discoveries[:5]:
                print(f"   • {d['repo']}/{d['file']}")
                print(f"     {len(d['secrets'])} secrets: ", end='')
                types = list(set(s['pattern'] for s in d['secrets']))
                print(', '.join(types[:3]))
        
        print(f"\n📄 Report: {report_file}")

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT first")
        exit(1)
    
    recon = GistRecon()
    recon.run_discovery()
