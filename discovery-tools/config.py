"""
Discovery Tool Configuration
IoT/ICS Taxonomy for OSINT scanning
"""

# Device categories with search terms and risk levels
IOT_TAXONOMY = {
    "industrial_control": {
        "description": "SCADA, PLCs, and industrial control systems",
        "risk_level": "critical",
        "search_terms": [
            "modbus port:502",
            "mqtt port:1883",
            "bacnet port:47808",
            "ethernet/ip port:44818",
            "s7comm port:102",
            "iec-104 port:2404",
            "dnp3 port:20000",
            "profinet",
            "scada",
            "plc",
            "rtu",
            "hmi",
            "siemens",
            "schneider electric",
            "rockwell",
            "allen-bradley",
            "mitsubishi",
            "omron",
            "wonderware",
            "ge fanuc"
        ]
    },
    "medical_devices": {
        "description": "Hospital equipment and medical IoT",
        "risk_level": "critical",
        "search_terms": [
            "dicom",
            "hl7",
            "pacs server",
            "hospital",
            "patient monitor",
            "mri",
            "ct scanner",
            "dialysis",
            "ventilator",
            "medical device",
            "philips healthcare",
            "ge healthcare"
        ]
    },
    "cameras_security": {
        "description": "IP cameras and surveillance systems",
        "risk_level": "high",
        "search_terms": [
            "webcam",
            "axis camera",
            "hikvision",
            "dahua",
            "cisco video surveillance",
            "panasonic security",
            "samsung techwin",
            "mobotix",
            "avigilon",
            "ip camera",
            "cctv",
            "surveillance",
            "dvr nvr",
            "blue iris",
            "zone minder"
        ]
    },
    "network_infrastructure": {
        "description": "Routers, firewalls, network equipment",
        "risk_level": "high",
        "search_terms": [
            "router",
            "firewall",
            "cisco asa",
            "palo alto",
            "fortinet",
            "juniper",
            "mikrotik",
            "ubiquiti",
            "netgear",
            "linksys",
            "d-link",
            "vpn concentrator",
            "load balancer",
            "switch managed"
        ]
    },
    "building_automation": {
        "description": "HVAC, lighting, and smart building systems",
        "risk_level": "medium",
        "search_terms": [
            "bacnet",
            "knx",
            "lonworks",
            "hvac control",
            "thermostat",
            "nest",
            "ecobee",
            "building automation",
            "bms",
            "lighting control",
            "access control",
            "intercom",
            "elevator control"
        ]
    },
    "vehicles_transport": {
        "description": "Connected vehicles and transport systems",
        "risk_level": "medium",
        "search_terms": [
            "tesla",
            "teslamate",
            "vehicle telematics",
            "gps tracker",
            "fleet management",
            "obd2",
            "toll system",
            "parking system",
            "ev charging",
            "traffic control"
        ]
    },
    "misc_iot": {
        "description": "Miscellaneous connected devices",
        "risk_level": "medium",
        "search_terms": [
            "printer",
            "hp jetdirect",
            "network printer",
            "nas",
            "synology",
            "qnap",
            "iot gateway",
            "smart home",
            "home assistant",
            "homekit",
            "zigbee bridge",
            "z-wave",
            "wifi thermostat",
            "smart lock",
            "doorbell",
            "robot vacuum"
        ]
    }
}

# GitHub dork patterns for credential exposure
GITHUB_DORKS = {
    "api_keys": [
        "sk_live_" "stripe",
        "AKIA" "aws_access_key_id",
        "apikey" "api_key" "api-key",
        "private_key" "private-key",
        "password" "passwd" "pwd",
        "secret" "secret_key" "secret-key",
        "token" "access_token" "auth_token"
    ],
    "config_files": [
        "filename:.env",
        "filename:.htaccess",
        "filename:config.json",
        "filename:config.yml",
        "filename:config.yaml",
        "filename:database.yml",
        "filename:credentials.xml",
        "filename:id_rsa",
        "filename:id_dsa",
        "filename:shadow",
        "filename:passwd"
    ],
    "database_creds": [
        "mysql_password", "mysql user",
        "postgres_password", "postgresql password",
        "mongodb_uri", "mongodb+srv",
        "redis_password", "redis auth"
    ],
    "cloud_configs": [
        "filename:aws.yml",
        "filename:azure.json",
        "filename:gcp.json",
        "filename:terraform.tfvars",
        "filename:credentials.json"
    ]
}

# crt.sh endpoints
CRTSH_URLS = {
    "subdomains": "https://crt.sh/?q=%.{domain}&output=json",
    "id_lookup": "https://crt.sh/?id={id}",
}
