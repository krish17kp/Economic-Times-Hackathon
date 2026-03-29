import sys
import logging
from fastapi.testclient import TestClient
from app.main import app

logging.basicConfig(level=logging.DEBUG)

client = TestClient(app)

response = client.post(
    "/api/v1/compare",
    json={
        "waste_type": "wheat_straw",
        "quantity_kg": 5000,
        "quality": "dry",
        "latitude": 30.73,
        "longitude": 76.77
    }
)

print(response.status_code)
print(response.json())
