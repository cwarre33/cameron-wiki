#!/usr/bin/env python3
"""
GitHub Dorks Scanner - Python Implementation
Searches for exposed credentials and sensitive data in public repos
"""

import requests
import json
import time
import base64
from pathlib import Path
from urllib.parse import quote_plus

class GitHubDorksScanner:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.base_url = "https://api.github.com"
        self.results = []
    
    def search_code(self, query, max_results=100):
        """Search GitHub code (requires authentication for higher rate limits)"""
        url = f"{self.base_url}/search/code"
        params = {"q": query, "per_page": min(max_results, 100)}
        
        try:
            resp = requests.get(url, params=params, timeout=30)
            if resp.status_code == 403:
                print(f"[!] Rate limited on query: {query}")
                return []
            resp.raise_for_status()
            data = resp.json()
            return data.get("items", [])
        except Exception as e:
            print(f"[!] Error searching '{query}': {e}")
            return []
    
    def scan_single_dork(self, dork, category, max_results=30):
        """Scan a single dork pattern"""
        print(f"[*] Scanning: {dork[:50]}...")
        items = self.search_code(dork, max_results)
        
        findings = []
        for item in items:
            finding = {
                "dork": dork,
                "category": category,
                "repo": item.get("repository", {}).get("full_name"),
                "file": item.get("name"),
                "path": item.get("path"),
                "url": item.get("html_url"),
                "score": item.get("score"),
                "language": item.get("language")
            }
            findings.append(finding)
        
        print(f"  [+] Found {len(findings)} results")
        return findings
    
    def scan_category(self, category_name, dorks, max_per_dork=20):
        """Scan a whole category of dorks"""
        print(f"\n[*] Scanning category: {category_name}")
        all_findings = []
        
        for dork in dorks:
            findings = self.scan_single_dork(dork, category_name, max_per_dork)
            all_findings.extend(findings)
            time.sleep(2)  # Rate limit respect
        
        # Save category results
        output_file = self.data_dir / f"github_{category_name}.json"
        with open(output_file, "w") as f:
            json.dump(all_findings, f, indent=2)
        
        print(f"[+] Saved {len(all_findings)} total findings to {output_file}")
        return all_findings
    
    def validate_finding(self, finding):
        """
        Heuristic validation - check if finding is likely a real exposure
        vs. false positive (like example code, test fixtures)
        """
        path = finding.get("path", "").lower()
        repo = finding.get("repo", "").lower()
        file_name = finding.get("file", "").lower()
        
        false_positive_markers = [
            "example", "sample", "test", "fixture", "mock", "demo",
            "dummy", "placeholder", "template", "tutorial"
        ]
        
        suspicious_paths = [
            ".env", "config", "credentials", "secret", "key",
            "password", "token", "auth", "private"
        ]
        
        # Check for false positive markers
        if any(marker in path or marker in repo or marker in file_name 
               for marker in false_positive_markers):
            return False
        
        # Check for suspicious patterns that increase confidence
        if any(pattern in path.lower() for pattern in suspicious_paths):
            finding["confidence"] = "high"
            return True
        
        finding["confidence"] = "medium"
        return True
    
    def generate_report(self):
        """Generate a summary report of findings"""
        # Load all github results
        all_findings = []
        for json_file in self.data_dir.glob("github_*.json"):
            with open(json_file) as f:
                data = json.load(f)
                all_findings.extend(data)
        
        # Validate and categorize
        validated = [f for f in all_findings if self.validate_finding(f)]
        
        report = {
            "total_findings": len(all_findings),
            "validated_findings": len(validated),
            "by_confidence": {
                "high": len([f for f in validated if f.get("confidence") == "high"]),
                "medium": len([f for f in validated if f.get("confidence") == "medium"])
            },
            "by_category": self._categorize_findings(validated),
            "high_priority": [f for f in validated if f.get("confidence") == "high"][:50]
        }
        
        # Save report
        report_file = self.data_dir / "github_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _categorize_findings(self, findings):
        """Categorize by dork category"""
        categories = {}
        for f in findings:
            cat = f.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        return categories

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "..")
    from config import GITHUB_DORKS
    
    scanner = GitHubDorksScanner()
    
    # Scan a few representative dorks (avoid rate limits)
    if len(sys.argv) > 1:
        # Single dork mode
        dork = sys.argv[1]
        findings = scanner.scan_single_dork(dork, "custom")
        for f in findings[:5]:
            print(f"  - {f['repo']}/{f['path']}")
    else:
        # Scan first category only (to avoid rate limits)
        if "api_keys" in GITHUB_DORKS:
            scanner.scan_category("api_keys", GITHUB_DORKS["api_keys"][:5])
            scanner.generate_report()
