#!/usr/bin/env python3
"""
Frequency Mapper - Aggregates discovery data
Creates visualization-ready data structures from scan results
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class FrequencyMapper:
    def __init__(self, data_dir="../data", output_dir="../output"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def load_shodan_data(self):
        """Load all Shodan scan results"""
        all_data = {}
        pattern = "shodan_*.json"
        
        for json_file in self.data_dir.glob(pattern):
            if "_full_" in json_file.name:
                continue  # Skip combined files
            
            with open(json_file) as f:
                data = json.load(f)
                category = json_file.stem.replace("shodan_", "")
                all_data[category] = data
        
        return all_data
    
    def aggregate_by_country(self, shodan_data):
        """Aggregate device counts by country across categories"""
        country_totals = defaultdict(dict)
        
        for category, data in shodan_data.items():
            stats = data.get("stats", {})
            countries = stats.get("country", [])
            
            for entry in countries:
                country = entry.get("name")
                count = entry.get("count", 0)
                
                if country not in country_totals:
                    country_totals[country] = {"total": 0, "by_category": {}}
                
                country_totals[country]["total"] += count
                country_totals[country]["by_category"][category] = count
        
        # Sort by total count
        sorted_countries = dict(sorted(
            country_totals.items(),
            key=lambda x: x[1]["total"],
            reverse=True
        ))
        
        return sorted_countries
    
    def aggregate_by_org(self, shodan_data):
        """Aggregate device counts by organization/ISP"""
        org_totals = defaultdict(dict)
        
        for category, data in shodan_data.items():
            stats = data.get("stats", {})
            orgs = stats.get("org", [])
            
            for entry in orgs:
                org = entry.get("name")
                count = entry.get("count", 0)
                
                if org not in org_totals:
                    org_totals[org] = {"total": 0, "by_category": {}}
                
                org_totals[org]["total"] += count
                org_totals[org]["by_category"][category] = count
        
        sorted_orgs = dict(sorted(
            org_totals.items(),
            key=lambda x: x[1]["total"],
            reverse=True
        )[:100])  # Top 100
        
        return sorted_orgs
    
    def create_device_frequency_map(self):
        """Create the main 'wow' visualization data"""
        print("[*] Creating device frequency map...")
        
        shodan_data = self.load_shodan_data()
        
        frequency_map = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "tool": "IoT/ICS Frequency Mapper",
                "data_source": "Shodan (free tier)"
            },
            "summary": self._create_summary(shodan_data),
            "categories": self._categorize_devices(shodan_data),
            "geography": {
                "by_country": self.aggregate_by_country(shodan_data)
            },
            "organizations": {
                "by_org": self.aggregate_by_org(shodan_data)
            },
            "risk_analysis": self._analyze_risk(shodan_data)
        }
        
        # Save frequency map
        output_file = self.output_dir / "device_frequency_map.json"
        with open(output_file, "w") as f:
            json.dump(frequency_map, f, indent=2)
        
        print(f"[+] Frequency map saved to {output_file}")
        self._print_summary(frequency_map)
        
        return frequency_map
    
    def _create_summary(self, data):
        """Create top-level summary"""
        total_queries = sum(d.get("total_queries", {}).get("queries", {}).get("__total__", 0) 
                           for d in data.values())
        
        summary = {
            "total_categories": len(data),
            "total_exposed_devices": total_queries,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "critical_infrastructure": "industrial_control" in data
        }
        
        return summary
    
    def _categorize_devices(self, data):
        """Create per-category breakdown"""
        categories = {}
        
        for cat_name, cat_data in data.items():
            queries = cat_data.get("queries", {})
            total = sum(v for v in queries.values() if isinstance(v, int))
            
            categories[cat_name] = {
                "total_devices": total,
                "top_devices": dict(sorted(
                    queries.items(),
                    key=lambda x: x[1] if isinstance(x[1], int) else 0,
                    reverse=True
                )[:10]),
                "risk_level": "critical" if cat_name in ["industrial_control", "medical_devices"] else "high" if cat_name in ["cameras_security"] else "medium"
            }
        
        return dict(sorted(
            categories.items(),
            key=lambda x: x[1]["total_devices"],
            reverse=True
        ))
    
    def _analyze_risk(self, data):
        """Generate risk analysis"""
        risky_devices = []
        
        critical_terms = [
            "modbus", "scada", "plc", "hmi", "bacnet", "s7comm",
            "dicom", "pacs", "hospital", "patient"
        ]
        
        for cat_name, cat_data in data.items():
            queries = cat_data.get("queries", {})
            for term, count in queries.items():
                if isinstance(count, int) and count > 100:
                    is_critical = any(ct in term.lower() for ct in critical_terms)
                    if is_critical:
                        risky_devices.append({
                            "device_type": term,
                            "category": cat_name,
                            "exposed_count": count,
                            "risk_tier": "critical" if count > 1000 else "high"
                        })
        
        return sorted(risky_devices, key=lambda x: x["exposed_count"], reverse=True)[:50]
    
    def _print_summary(self, freq_map):
        """Print pretty summary"""
        print("\n" + "=" * 60)
        print("IoT/ICS DISCOVERY SUMMARY")
        print("=" * 60)
        
        print("\n📊 Categories:")
        for cat, data in freq_map["categories"].items():
            print(f"  {cat.replace('_', ' ').title()}: {data['total_devices']:,} devices")
            print(f"    Risk: {data['risk_level'].upper()}")
            if data["top_devices"]:
                top = list(data["top_devices"].items())[0]
                print(f"    Most common: {top[0]} ({top[1]:,})")
        
        print("\n🌍 Top Countries:")
        for country, data in list(freq_map["geography"]["by_country"].items())[:10]:
            print(f"  {country}: {data['total']:,} devices")
        
        print("\n⚠️ Highest Risk Exposures:")
        for device in freq_map["risk_analysis"][:10]:
            print(f"  {device['device_type']} ({device['category']}): {device['exposed_count']:,} exposed")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    mapper = FrequencyMapper()
    mapper.create_device_frequency_map()
