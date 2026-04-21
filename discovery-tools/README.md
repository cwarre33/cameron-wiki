# Discovery Tools for OSINT

IoT/ICS security discovery suite. FREE tools only.

## Structure

```
discovery-tools/
├── config.py                 # IoT taxonomy and search definitions
├── modules/
│   ├── cert_discovery.py     # SSL cert transparency (crt.sh)
│   ├── shodan_profiler.py    # Free Shodan stats/count
│   ├── github_dorks.py       # Exposed cred search
│   └── frequency_mapper.py   # Data aggregator
├── output/
│   ├── shodan_iot_full_*.json    # Raw scan data
│   └── device_frequency_map.json  # Aggregated data
├── discover-dashboard.html   # Interactive visualization
│                             └── Open in browser to explore
└── README.md
```

## Usage

### Shodan Profiling (Free Tier)

```bash
cd modules
python3 shodan_profiler.py   # Full IoT scan using counts/stats
```

Uses `shodan count` and `shodan stats` (free), not `search` (costs credits).

### Certificate Transparency Scanning

```bash
cd modules
python3 cert_discovery.py example.com
```

### GitHub Dorks

```bash
cd modules
python3 github_dorks.py     # Scan for exposed credentials
```

⚠️ **Rate limits**: ~60 req/hour unauthenticated. Use sparingly.

### Generate Frequency Map

```bash
cd modules
python3 frequency_mapper.py   # Consolidate into visualization data
```

### View Dashboard

Open `discover-dashboard.html` in a browser for interactive exploration of IoT exposure frequencies.

## Data Ethics

- Findings are NOT actionable exploitation targets
- For responsible disclosure planning only
- Never touch discovered systems
- Report through proper channels only

## Key Discoveries from Current Scan

| Category | Exposed Devices | Risk |
|----------|-----------------|------|
| IP Cameras | ~5.79M | High |
| Network Infrastructure | ~7.4M | High |
| Industrial Control | ~537K | **Critical** |
| Medical Devices | ~11K | **Critical** |

Top risks:
- **MQTT** (IoT messaging): 452K+ exposed brokers
- **Hikvision cameras**: 2.27M exposed
- **Mikrotik routers**: 3.69M exposed
- **DICOM medical servers**: 6,854 worldwide

See `output/` for full raw data.
