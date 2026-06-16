import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to NEXUS VIDEO AGENT API"}

def test_get_status_not_found():
    response = client.get("/api/status/invalid-id")
    assert response.status_code == 404
