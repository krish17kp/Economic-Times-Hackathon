import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'http://localhost:8000/api/v1/compare',
    data=json.dumps({'waste_type': 'wheat_straw', 'quantity_kg': 5000, 'quality': 'dry', 'latitude': 30.73, 'longitude': 76.77}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    res = urllib.request.urlopen(req)
    out = res.read().decode('utf-8')
except urllib.error.HTTPError as e:
    out = e.read().decode('utf-8')

with open('output_err.json', 'w', encoding='utf-8') as f:
    f.write(out)
