import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Verify health check endpoint status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_without_tenant_header():
    """Verify request fails when X-Tenant-ID header is missing."""
    payload = {
        "features": [0.1, 0.5, 0.2, 0.8, 0.3],
        "max_risk_threshold": 0.70
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 400
    assert "Missing X-Tenant-ID" in response.json()["detail"]

def test_predict_valid_request():
    """Verify complete end-to-end prediction and verification pipeline."""
    headers = {"X-Tenant-ID": "11111111-1111-1111-1111-111111111111"}
    payload = {
        "features": [0.1, 0.2, 0.3, 0.1, 0.2],
        "max_risk_threshold": 0.95
    }
    response = client.post("/api/v1/predict", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == "11111111-1111-1111-1111-111111111111"
    assert "constraint_passed" in data
    assert "attributions" in data