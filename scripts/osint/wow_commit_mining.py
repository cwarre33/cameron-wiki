#!/usr/bin/env python3
"""
WOW Recon - Commit History Mining (Option C)

Searches git commit history for secrets that were deleted but still exist in history.
This is where the real gems hide - people think deleting the file removes the secret!
"""

import os
import json
import base64
import requests
import re
from datetime import datetime
from pathlib import Path

class CommitHistoryRecon:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.discoveries = []
        self.secrets_found = 0
        
    def search_commits(self, query, max_items=20):
        """Search for commits containing patterns in message or diff"""
        url = "https://api.github.com/search/commits"
        params = {
            'q': query,
            'sort': 'committer-date',
            'order': 'desc',
            'per_page': max_items
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json().get('items', [])
        except Exception as e:
            print(f"  Search error: {e}")
        return []
    
    def get_commit_diff(self, repo_full_name, commit_sha):
        """Get the actual diff of a commit - where secrets often appear in red (-)"""
        url = f"https://api.github.com/repos/{repo_full_name}/commits/{commit_sha}"
        
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"  Error getting commit: {e}")
        return None
    
    def get_file_from_commit(self, repo_full_name, commit_sha, file_path):
        """Get file content from a specific commit"""
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}?ref={commit_sha}"
        
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('content'):
                    return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
        except Exception:
            pass
        return None
    
    def extract_secrets_from_text(self, text, context='commit'):
        """Extract credential patterns from text"""
        findings = []
        
        # These patterns look for actual credential formats
        patterns = [
            # AWS - Look for AKIA pattern + access key
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
            
            # MongoDB connection string - the most leaked credential type
            (r'mongodb(\+srv)?://[^:]+:([^@]+)@[^\s\"'';]+', 'MongoDB Connection String'),
            
            # Database URLs with real creds
            (r'(postgres|mysql)://[^:]+:([^@]+)@[^\s\"'';]+', 'Database URL'),
            
            # API keys - common prefixes
            (r'(api[_-]?key|apikey)[\s]*[=:][\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?', 'API Key'),
            
            # JWT secrets
            (r'(jwt[_-]?secret|secret[_-]?jwt)[\s]*[=:][\s]*["\']?([a-zA-Z0-9!@#$%^&*-_=+]{16,})["\']?', 'JWT Secret'),
            
            # Generic password patterns that look real
            (r'password[\s]*[=:][\s]*["\']([*A-Za-z0-9!@#$%^&*]{12,})["\']', 'Password'),
            
            # Firebase
            (r'AIza[0-9A-Za-z_-]{35}', 'Firebase API Key'),
            
            # SendGrid
            (r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}', 'SendGrid API Key'),
            
            # Slack
            (r'(xoxb|xoxa|xoxp)-[0-9]+-[0-9-]+-[a-zA-Z0-9]+', 'Slack Token'),
            
            # Stripe
            (r'sk_(live|test)_[a-zA-Z0-9]{24,}', 'Stripe API Key'),
            
            # Private keys (PEM format)
            (r'-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----[\s\S]{100,200}-----END', 'Private Key'),
        ]
        
        lines = text.split('\n')
        
        for pattern_name, pattern in patterns:
            # Search in entire text first
            for match in re.finditer(pattern, text):
                match_text = match.group(0)
                # Only count if it's not a placeholder/example
                if not self._is_placeholder(match_text):
                    findings.append({
                        'pattern': pattern_name,
                        'match': self._redact(match_text),
                        'context': context
                    })
                    self.secrets_found += 1
        
        return findings
    
    def _is_placeholder(self, text):
        """Check if text is likely a placeholder or example"""
        placeholders = ['example', 'fake', 'dummy', 'test', 'xyz', '123', 'aaaa', 'changeme', 
                        'your_', 'my_', 'password', 'INSERT', 'placeholder', 'none', 'null',
                        'undefined', 'todo', 'FIXME']
        
        text_lower = text.lower()
        return any(p in text_lower for p in placeholders)
    
    def _redact(self, text):
        """Redact sensitive parts but show format"""
        if len(text) < 20:
            return text[:4] + "***"
        return text[:12] + "***[REDACTED]***" + text[-4:]
    
    def run_discovery(self):
        """Main discovery workflow"""
        print("\n" + "🚨" * 30)
        print("        COMMIT HISTORY MINING")
        print("        Finding secrets in git history...")
        print(f"        Started: {datetime.now().strftime('%H:%M:%S')}")
        print("🚨" * 30)
        print()
        
        # Search for commits that removed .env files or added secrets
        searches = [
            # Commits that removed .env files - often where secrets were deleted
            {'query': 'remove .env', 'desc': 'Commits removing .env files'},
            {'query': 'delete .env', 'desc': 'Commits deleting .env files'},
            
            # Commits about secrets
            {'query': 'remove secret', 'desc': 'Commits removing secrets'},
            {'query': 'hide password', 'desc': 'Commits hiding credentials'},
            
            # Commits updating config
            {'query': 'update config password', 'desc': 'Config updates with passwords'},
            
            # Emergency commits
            {'query': 'remove token', 'desc': 'Token removal commits'},
            {'query': 'fix security', 'desc': 'Security fix commits'},
        ]
        
        all_commits = []
        
        for search in searches:
            print(f"🔍 {search['desc']}")
            commits = self.search_commits(search['query'], max_items=15)
            
            for commit in commits:
                repo = commit['repository']['full_name'] if 'repository' in commit else 'unknown'
                all_commits.append({
                    'repo': repo,
                    'sha': commit['sha'],
                    'message': commit['commit']['message'],
                    'author': commit['commit']['author']['name'],
                    'date': commit['commit']['author']['date'],
                })
        
        # Deduplicate commits
        seen = set()
        unique_commits = []
        for c in all_commits:
            key = c['sha']
            if key not in seen:
                seen.add(key)
                unique_commits.append(c)
        
        print(f"\n🎯 Found {len(unique_commits)} unique commits to investigate")
        print("=" * 60)
        
        # Analyze top commits
        for commit in unique_commits[:10]:
            repo = commit['repo']
            sha = commit['sha']
            
            print(f"\n📜 {repo[:50]}...")
            print(f"   Commit: {sha[:8]}")
            print(f"   Message: {commit['message'][:60].replace(chr(10), ' ')}...")
            
            # Get the commit details
            commit_data = self.get_commit_diff(repo, sha)
            
            if commit_data:
                # Look at the files changed
                files = commit_data.get('files', [])
                
                for file in files[:3]:  # Check up to 3 files
                    filename = file.get('filename', '')
                    patch = file.get('patch', '')
                    
                    if patch and any(ext in filename.lower() for ext in ['.env', 'config', 'secret', 'key', '.json', '.yml', '.yaml', '.properties']):
                        print(f"   📄 Changed: {filename}")
                        
                        secrets = self.extract_secrets_from_text(patch, f"patch:{filename}")
                        
                        if secrets:
                            print(f"   🚨 FOUND {len(secrets)} SECRET(S) IN COMMIT!")
                            for s in secrets[:3]:
                                print(f"      → {s['pattern']}: {s['match']}")
                            
                            self.discoveries.append({
                                'repo': repo,
                                'commit': sha,
                                'file': filename,
                                'secrets': secrets,
                                'found_at': datetime.now().isoformat()
                            })
        
        self._save_report()
    
    def _save_report(self):
        """Save discovery report"""
        Path("reports").mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"reports/wow_commit_mining_{timestamp}.json"
        
        report = {
            'session': 'WOW Commit History Mining',
            'timestamp': datetime.now().isoformat(),
            'total_secrets_found': self.secrets_found,
            'commits_with_secrets': len(self.discoveries),
            'discoveries': self.discoveries
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 60)
        print("COMMIT MINING COMPLETE")
        print("=" * 60)
        print(f"Total secrets found: {self.secrets_found}")
        print(f"Commits with secrets: {len(self.discoveries)}")
        
        if self.discoveries:
            print("\n🔥 DISCOVERED COMMITS WITH SECRETS:")
            for d in self.discoveries[:5]:
                print(f"   • {d['repo'][:40]}... - {len(d['secrets'])} secrets")
        
        print(f"\n📄 Report saved: {report_file}")

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT first")
        exit(1)
    
    recon = CommitHistoryRecon()
    recon.run_discovery()
