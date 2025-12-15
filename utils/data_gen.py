import pandas as pd
import numpy as np
import random
import datetime

# --- GLOBAL THREAT INTELLIGENCE ---
# (Attack Type, Message, Detail)
ATTACK_TYPES = [
    ("CRIT", "SQL Injection", "payload=' OR 1=1--"),
    ("WARN", "SSH Brute Force", "User: root failed 5x"),
    ("CRIT", "Ransomware Activity", "File encryption .crypt detected"),
    ("BLOCK", "Botnet Traffic", "Known C2 Server Contacted"),
    ("INFO", "Admin Login", "Successful Auth via MFA"),
    ("WARN", "Port Scan", "Scanning Ports 22-8080"),
    ("CRIT", "XSS Payload", "<script>alert('pwned')</script>"),
    ("BLOCK", "DDoS Flood", "SYN Flood > 10k pps"),
    ("WARN", "Privilege Escalation", "Sudo usage without ticket"),
    ("BLOCK", "Geo-Fence Block", "Traffic from Sanctioned Region")
]

# (City, Country Code, IP Prefix)
LOCATIONS = [
    ("Moscow", "RU", "188.143"),
    ("Beijing", "CN", "202.108"),
    ("Pyongyang", "KP", "175.45"),
    ("Tehran", "IR", "5.200"),
    ("New York", "US", "45.33"),
    ("London", "UK", "81.2"),
    ("Berlin", "DE", "141.1"),
    ("Lagos", "NG", "197.210"),
    ("Mumbai", "IN", "103.20"),
    ("Sao Paulo", "BR", "200.10")
]
# Add these coordinates to your existing LOCATIONS list if needed, 
# or use this dedicated map dictionary.

MAP_LOCATIONS = [
    {"lat": 37.77, "lon": -122.41, "city": "San Francisco", "country": "US"},
    {"lat": 55.75, "lon": 37.61, "city": "Moscow", "country": "RU"},
    {"lat": 39.90, "lon": 116.40, "city": "Beijing", "country": "CN"},
    {"lat": 51.50, "lon": -0.12, "city": "London", "country": "UK"},
    {"lat": -22.90, "lon": -43.17, "city": "Rio de Janeiro", "country": "BR"},
    {"lat": 6.52, "lon": 3.37, "city": "Lagos", "country": "NG"},
    {"lat": 28.61, "lon": 77.20, "city": "New Delhi", "country": "IN"},
    {"lat": 35.68, "lon": 139.69, "city": "Tokyo", "country": "JP"},
    {"lat": 52.52, "lon": 13.40, "city": "Berlin", "country": "DE"},
    {"lat": -33.86, "lon": 151.20, "city": "Sydney", "country": "AU"}
]

def get_map_data(count=60):
    """Generates random attack events with JITTER for animation effect."""
    data = []
    for _ in range(count):
        loc = random.choice(MAP_LOCATIONS)
        
        # CRITICAL: This Jitter makes the dots move!
        # Increase the range (-5, 5) if you want MORE movement
        jitter_lat = random.uniform(-3, 3) 
        jitter_lon = random.uniform(-3, 3)
        
        data.append({
            "lat": loc["lat"] + jitter_lat,
            "lon": loc["lon"] + jitter_lon,
            "city": loc["city"],
            "country": loc["country"],
            "type": random.choice(["DDoS", "Malware", "SQL Injection", "Botnet"]),
            "attacks": random.randint(10, 500)
        })
    return pd.DataFrame(data)

# --- FUNCTIONS ---

def generate_random_ip(prefix):
    """Generates a realistic random IP based on a regional prefix."""
    return f"{prefix}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_random_log():
    """Constructs a single globally-aware log entry."""
    now = datetime.datetime.now()
    seconds_ago = random.randint(0, 300) # Fresh logs only
    log_time = (now - datetime.timedelta(seconds=seconds_ago)).strftime("%H:%M:%S")
    
    # Pick a random attack and a random location
    severity, attack, detail = random.choice(ATTACK_TYPES)
    city, country, ip_prefix = random.choice(LOCATIONS)
    ip = generate_random_ip(ip_prefix)
    
    # Example: [12:00:01] CRIT: SQL Injection - Moscow, RU (188.143.22.10)
    return f"[{log_time}] {severity}: {attack} ({detail}) - Origin: {city}, {country} ({ip})"

def get_dummy_logs(count=15):
    """Returns a list of 'count' procedurally generated logs."""
    logs = [generate_random_log() for _ in range(count)]
    logs.sort(reverse=True) 
    return logs

def get_attack_stats():
    """Generates dummy data for graphs."""
    return pd.DataFrame({
        'Hour': range(24),
        'Attacks': np.random.randint(5, 120, 24)
    })
