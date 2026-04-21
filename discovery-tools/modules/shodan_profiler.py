#!/usr/bin/env python3
"""
Shodan Profiler - Free query tools only
Uses count and stats commands (no search credits required)
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

class ShodanProfiler:
    def __init__(self, output_dir="../output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def _run_cmd(self, cmd_args):
        """Run a shodan CLI command"""
        try:
            result = subprocess.run(
                ["shodan"] + cmd_args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Timeout", 1
        except Exception as e:
            return "", str(e), 1
    
    def count(self, query):
        """Get count for a query (free)"""
        stdout, stderr, rc = self._run_cmd(["count", query])
        if rc == 0:
            # Parse the number from output
            match = re.search(r'(\d+)', stdout)
            if match:
                return int(match.group(1))
        return 0
    
    def stats(self, query, facets=None):
        """Get stats for a query (free)"""
        cmd = ["stats", query]
        if facets:
            cmd.extend(["--facets", facets])
        cmd.extend(["--limit", "20"])
        
        stdout, stderr, rc = self._run_cmd(cmd)
        if rc == 0:
            return self._parse_stats(stdout)
        return {"error": stderr}
    
    def _parse_stats(self, output):
        """Parse stats output into structured data"""
        sections = {}
        current_facet = None
        
        for line in output.split('\n'):
            line = line.strip()
            if "Facet:" in line:
                current_facet = line.split("Facet:")[-1].strip().lower().replace(' ', '_')
                sections[current_facet] = []
            elif current_facet and line:
                # Parse "Name         123" format
                match = re.match(r'^(\S.+?)\s+(\d+)$', line)
                if match:
                    sections[current_facet].append({
                        "name": match.group(1).strip(),
                        "count": int(match.group(2))
                    })
        
        return sections
    
    def honeyscore(self, ip):
        """Check honeypot probability for IP"""
        stdout, stderr, rc = self._run_cmd(["honeyscore", ip])
        if rc == 0:
            # Parse honeyscore output (usually gives percentage)
            return stdout
        return None
    
    def profile_iot_category(self, category_name, search_terms):
        """Profile an entire IoT category with multiple queries"""
        print(f"\n[*] Profiling {category_name}...")
        
        results = {
            "category": category_name,
            "timestamp": datetime.now().isoformat(),
            "queries": {},
            "totals": {}
        }
        
        for term in search_terms:
            count = self.count(term)
            term_clean = term.replace(' ', '_').replace(':', '_')
            results["queries"][term_clean] = count
            print(f"  - {term}: {count}")
        
        # Get stats for top query if it has results
        top_query = max(results["queries"].items(), key=lambda x: x[1])
        if top_query[1] > 0:
            print(f"  [*] Getting stats for {top_query[0]}...")
            stats = self.stats(search_terms[0], "country,org,port,product")
            results["stats"] = stats
        
        return results
    
    def full_iot_scan(self, taxonomy):
        """Scan all IoT categories"""
        print("=" * 60)
        print("Shodan IoT/ICS Frequency Mapper (Free Tools)")
        print("=" * 60)
        
        all_results = {}
        
        for category, config in taxonomy.items():
            results = self.profile_iot_category(
                category,
                config.get("search_terms", [])
            )
            all_results[category] = results
            
            # Save intermediate results
            output_file = self.output_dir / f"shodan_{category}.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
        
        # Save full scan
        full_file = self.output_dir / f"shodan_iot_full_{datetime.now().strftime('%Y%m%d')}.json"
        with open(full_file, "w") as f:
            json.dump(all_results, f, indent=2)
        
        print("\n" + "=" * 60)
        print(f"[+] Full scan saved to {full_file}")
        print("=" * 60)
        
        return all_results

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "..")
    from config import IOT_TAXONOMY
    
    profiler = ShodanProfiler()
    
    if len(sys.argv) > 1:
        # Single query mode
        print(f"[Count] {sys.argv[1]}: {profiler.count(sys.argv[1])}")
    else:
        # Full scan
        results = profiler.full_iot_scan(IOT_TAXONOMY)
