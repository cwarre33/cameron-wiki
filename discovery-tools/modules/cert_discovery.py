#!/usr/bin/env python3
"""
SSL Certificate Transparency Log Scanner
Uses crt.sh to discover subdomains and anomalies
"""

import requests
import json
import time
from urllib.parse import quote
from pathlib import Path

class CertDiscovery:
    def __init__(self, data_dir="../data"):
        self.base_url = "https://crt.sh"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def get_subdomains(self, domain):
        """Get all subdomains from crt.sh for a domain"""
        url = f"{self.base_url}/?q=%.{quote(domain)}&output=json"
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            # Extract unique subdomains
            subdomains = set()
            for entry in data:
                name = entry.get("name_value", "").strip()
                if name and "*" not in name:
                    subdomains.add(name)
                # Check SAN entries too
                san = entry.get("san", "")
                if san:
                    for s in san.split("\n"):
                        s = s.strip()
                        if s and "*" not in s:
                            subdomains.add(s)
            
            return sorted(subdomains)
        except Exception as e:
            print(f"Error fetching subdomains for {domain}: {e}")
            return []
    
    def find_anomalies(self, subdomains):
        """Find interesting/worrying subdomains"""
        interesting = {
            "high_risk": [],
            "admin_panels": [],
            "staging_dev": [],
            "services": [],
            "internal": []
        }
        
        risk_patterns = {
            "high_risk": ["admin", "manage", "panel", "root", "system", "api", "backend"],
            "admin_panels": ["cpanel", "whm", "plesk", "admin", "dashboard", "control"],
            "staging_dev": ["staging", "dev", "test", "beta", "uat", "qa", "preview"],
            "services": ["jenkins", "git", "gitlab", "github", "bitbucket", "jira", "confluence"],
            "internal": ["internal", "corp", "intranet", "inside", "private", "vpn"]
        }
        
        for subdomain in subdomains:
            sub_lower = subdomain.lower()
            for category, patterns in risk_patterns.items():
                if any(pat in sub_lower for pat in patterns):
                    interesting[category].append(subdomain)
                    break
        
        return interesting
    
    def scan_domain(self, domain):
        """Full scan of a domain"""
        print(f"[*] Scanning {domain} via crt.sh...")
        subdomains = self.get_subdomains(domain)
        anomalies = self.find_anomalies(subdomains)
        
        result = {
            "domain": domain,
            "total_subdomains": len(subdomains),
            "subdomains": subdomains,
            "anomalies": anomalies
        }
        
        # Save to file
        output_file = self.data_dir / f"{domain}_subdomains.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"[+] Found {len(subdomains)} subdomains")
        print(f"[+] Anomalies: High-risk: {len(anomalies['high_risk'])}, "
              f"Admin: {len(anomalies['admin_panels'])}, "
              f"Staging: {len(anomalies['staging_dev'])}, "
              f"Services: {len(anomalies['services'])}, "
              f"Internal: {len(anomalies['internal'])}")
        
        return result

if __name__ == "__main__":
    import sys
    scanner = CertDiscovery()
    if len(sys.argv) > 1:
        scanner.scan_domain(sys.argv[1])
    else:
        print("Usage: python cert_discovery.py <domain>")
