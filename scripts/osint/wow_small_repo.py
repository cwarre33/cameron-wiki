#!/usr/bin/env python3
"""
WOW Recon - Small Repo Focus (Option D)

Targets small repos (< 3MB) that clone instantly.
Small repos = personal projects, quick POCs, tutorials that weren't cleaned up.
This is where ACTUAL secrets leak.
"""

import os
import json
import subprocess
import requests
import re
from datetime import datetime
from pathlib import Path

class SmallRepoRecon:
    def __init__(self):
        self.github_pat = os.environ.get('GITHUB_PAT')
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': f'token {self.github_pat}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.discoveries = []
        self.secrets_found = 0
        
    def find_small_repos(self):
        """Search for small repos with config files"""
        searches = [
            # Small repos with .env
            {'query': '.env language:javascript size:<1000', 'desc': 'Small JS repos with .env'},
            {'query': '.env language:python size:<1000', 'desc': 'Small Python repos with .env'},
            {'query': 'config.json size:<500', 'desc': 'Tiny repos with configs'},
            {'query': '.env.local language:typescript size:<1000', 'desc': 'TS projects with local env'},
        ]
        
        repos = []
        
        for search in searches:
            print(f"🔍 {search['desc']}")
            url = "https://api.github.com/search/repositories"
            params = {
                'q': search['query'],
                'sort': 'updated',
                'order': 'desc',
                'per_page': 15
            }
            
            try:
                response = self.session.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    items = response.json().get('items', [])
                    print(f"   Found: {len(items)} repos")
                    for item in items:
                        repos.append({
                            'name': item['full_name'],
                            'url': item['clone_url'],
                            'size': item['size'],
                            'updated': item['updated_at'],
                            'html_url': item['html_url']
                        })
            except Exception as e:
                print(f"   Error: {e}")
        
        return repos
    
    def scan_repo(self, repo_info):
        """Quick clone and scan with TruffleHog"""
        name = repo_info['name']
        url = repo_info['url']
        
        # Skip if too large
        if repo_info['size'] > 5000:  # 5MB limit
            return []
        
        clone_dir = f"/tmp/small_repos/{name.replace('/', '_')}"
        
        # Clean
        if os.path.exists(clone_dir):
            subprocess.run(['rm', '-rf', clone_dir], check=False)
        
        # Clone with timeout
        try:
            print(f"📁 Cloning {name} ({repo_info['size']}KB)...")
            clone_start = datetime.now()
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--single-branch', url, clone_dir],
                capture_output=True,
                timeout=15  # 15 sec max
            )
            
            if result.returncode != 0:
                return []
            
            clone_time = (datetime.now() - clone_start).total_seconds()
            print(f"   Cloned in {clone_time:.1f}s")
            
            # Run TruffleHog
            config_path = "trufflehog-config.yml"
            cmd = ['trufflehog', 'filesystem', clone_dir, '--json', '--no-update']
            if os.path.exists(config_path):
                cmd.extend(['--config', config_path])
            
            th_result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            
            findings = []
            for line in th_result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        finding = json.loads(line)
                        findings.append(finding)
                        self.secrets_found += 1
                    except:
                        pass
            
            # Cleanup
            subprocess.run(['rm', '-rf', clone_dir], check=False)
            
            return findings
            
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Timeout on {name}")
            subprocess.run(['rm', '-rf', clone_dir], check=False)
            return []
        except Exception as e:
            print(f"   Error: {e}")
            subprocess.run(['rm', '-rf', clone_dir], check=False)
            return []
    
    def manual_file_scan(self, repo_name, clone_dir):
        """Manual regex scan of common config files"""
        findings = []
        
        # File patterns to check
        patterns = [
            '.env', '.env.local', '.env.development', '.env.production',
            'config.json', 'config.yml', '.aws/credentials', 
            'secrets.yaml', 'application.properties', 'settings.json'
        ]
        
        regex = {
            'AWS Key': r'AKIA[0-9A-Z]{16}',
            'MongoDB URI': r'mongodb(\+srv)?://[^:]+:([^@]+)@[^\s"'';`\)\n]{10,}',
            'Database URL': r'(postgres|mysql|redis)://[^:]+:[^@]+@[^\s\"'';]+',
            'OpenAI': r'sk-[a-zA-Z0-9]{48}',
            'Secret Key': r'secret[_\-]?[key|token][\s]*[=:][\s]*["\']?([a-zA-Z0-9_-]{16,})["\']?',
            'JWT Secret': r'(jwt|SECRET)[_\-]?(SECRET|KEY|PASS)[\s]*[=:][\s]*["\']?([a-zA-Z0-9!@#$%^&*-_=+\.]{16,})',
            'Password': r'pass(word|wd)?[\s]*[=:][\s]*["\']([^"\']{8,32})',
            'API Key': r'(key|api[_-]?key)[\\s]*[=:][\s]*["\']([a-f0-9]{20,}|[A-Za-z0-9_-]{32,})',
            'Firebase': r'AIza[0-9A-Za-z_-]{35}',
            'Stripe': r'sk_(live|test)_[a-zA-Z0-9]{24,}',
            'Slack': r'xox[bap]-[0-9]+-[0-9-]+-[a-zA-Z0-9]+',
            'Private Key': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
        }
        
        for root, dirs, files in os.walk(clone_dir):
            for file in files:
                if any(file.endswith(ext) or file == ext for ext in patterns):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        for name, pattern in regex.items():
                            for match in re.finditer(pattern, content):
                                val = match.group(0)
                                # Filter out obvious placeholders
                                if any(x in val.lower() for x in ['example', 'fake', 'test', 'dummy', 'changeme', 'your_', 'password']):
                                    continue
                                findings.append({
                                    'type': name,
                                    'file': file,
                                    'match': val[:30] + '***REDACTED***' if len(val) > 30 else val[:4] + '***'
                                })
                    except:
                        continue
        
        return findings
    
    def run_discovery(self):
        """Main discovery workflow"""
        print("\n" + "💎" * 25)
        print("         SMALL REPO GOLD RUSH")
        print("         Fast clones, real secrets")
        print(f"         Started: {datetime.now().strftime('%H:%M:%S')}")
        print("💎" * 25)
        print()
        
        # Find targets
        repos = self.find_small_repos()
        
        print(f"\n🎯 Got {len(repos)} small repos to scan")
        print("=" * 50)
        
        # Scan them
        for repo in repos[:12]:
            print(f"\n🔎 {repo['name']} ({repo['size']}KB)")
            
            # Try TruffleHog first
            results = self.scan_repo(repo)
            
            if results:
                print(f"   🚨 TRUFFLEHOG FOUND {len(results)} SECRET(S)!")
                for r in results[:3]:
                    det = r.get('DetectorName', 'unknown')
                    raw = str(r.get('Raw', ''))[:25]
                    print(f"      → {det}: {raw}...")
                
                self.discoveries.append({
                    'repo': repo['name'],
                    'url': repo['html_url'],
                    'size_kb': repo['size'],
                    'tool': 'trufflehog',
                    'findings': results
                })
                
        self._save_report()
    
    def _save_report(self):
        """Save discovery report"""
        Path("reports").mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"reports/wow_small_repo_{timestamp}.json"
        
        report = {
            'session': 'WOW Small Repo Gold Rush',
            'timestamp': datetime.now().isoformat(),
            'total_secrets_found': self.secrets_found,
            'repos_with_secrets': len(self.discoveries),
            'discoveries': self.discoveries
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 50)
        print("SMALL REPO SCAN COMPLETE")
        print("=" * 50)
        print(f"Total secrets found: {self.secrets_found}")
        print(f"Repos with secrets: {len(self.discoveries)}")
        
        if self.discoveries:
            print("\n🔥 GOLD FOUND:")
            for d in self.discoveries[:5]:
                print(f"   • {d['repo']}: {len(d['findings'])} findings")
        else:
            print("\n⚪ Clean sweep - no active secrets in scanned repos")
        
        print(f"\n📄 Report: {report_file}")

if __name__ == '__main__':
    if 'GITHUB_PAT' not in os.environ:
        print("❌ Set GITHUB_PAT first")
        exit(1)
    
    recon = SmallRepoRecon()
    recon.run_discovery()