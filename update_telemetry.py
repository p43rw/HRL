#!/usr/bin/env python3
import os
import json
import subprocess
import urllib.request
from datetime import datetime, timezone

# Ensure working directory is the repository root
os.chdir('/etc/HRL')

print(f"[{datetime.now(timezone.utc)}] Starting telemetry poll...")

# 1. Fetch HamQsl XML & NOAA Boulder JSON
try:
    req = urllib.request.urlopen('https://www.hamqsl.com/solarxml.php', timeout=15)
    with open('solar-cache.xml', 'w') as f:
        f.write(req.read().decode('utf-8'))
    print('Successfully fetched HamQsl XML')
except Exception as e:
    print(f'Error fetching HamQsl: {e}')

try:
    req = urllib.request.urlopen('https://services.swpc.noaa.gov/json/boulder_k_index_1m.json', timeout=15)
    with open('boulder-cache.json', 'w') as f:
        f.write(req.read().decode('utf-8'))
    print('Successfully fetched NOAA Boulder JSON')
except Exception as e:
    print(f'Error fetching Boulder K-index: {e}')

# 2. Fetch Tropospheric Ducting Forecast
locations = {
    'EU-W': {'lat': 52.1, 'lon': 5.1, 'name': 'Western Europe (North Sea / UK)'},
    'US-E': {'lat': 40.7, 'lon': -74.0, 'name': 'US Northeast & Mid-Atlantic'},
    'US-W': {'lat': 37.7, 'lon': -122.4, 'name': 'US West Coast / Pacific'}
}

tropo_results = []
for code, loc in locations.items():
    url = f'https://api.open-meteo.com/v1/forecast?latitude={loc["lat"]}&longitude={loc["lon"]}&hourly=pressure_msl,relative_humidity_2m&forecast_days=1'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'HamRadioLive-Bot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            hourly = data.get('hourly', {})
            pressures = hourly.get('pressure_msl', [1013])
            humidities = hourly.get('relative_humidity_2m', [50])
            
            cur_p = pressures[0] if pressures else 1013
            cur_h = humidities[0] if humidities else 50
            
            p_score = max(0, min(50, (cur_p - 1013) * 4))
            h_score = max(0, (100 - cur_h) * 0.3)
            total_score = int(min(100, max(10, p_score + h_score + 15)))
            
            status = 'Verified Active Opening (Level 3)' if total_score >= 70 else ('Moderate Ducting (Level 2)' if total_score >= 40 else 'Normal / Weak (Level 1)')
            
            tropo_results.append({
                'region_code': code,
                'name': loc['name'],
                'pressure': cur_p,
                'score': total_score,
                'status': status,
                'live_verified': True
            })
    except Exception as e:
        print(f'Error fetching tropo for {code}: {e}')
        tropo_results.append({
            'region_code': code,
            'name': loc['name'],
            'pressure': 1013,
            'score': 15,
            'status': 'Normal / Weak (Level 1)',
            'live_verified': False
        })

output = {
    'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
    'regions': tropo_results
}

with open('tropo-cache.json', 'w') as f:
    json.dump(output, f, indent=2)
print('Successfully generated tropo-cache.json')

# 3. Git Commit and Push
subprocess.run(['git', 'add', 'solar-cache.xml', 'boulder-cache.json', 'tropo-cache.json'], check=False)

# Check if there are changes staged
status_res = subprocess.run(['git', 'diff', '--quiet', '--staged'], capture_output=True)
if status_res.returncode != 0:
    subprocess.run(['git', 'commit', '-m', 'Auto-update telemetry cache from reverseproxy [skip ci]'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print('Successfully committed and pushed telemetry updates.')
else:
    print('No changes detected in cache files. Skipping push.')
