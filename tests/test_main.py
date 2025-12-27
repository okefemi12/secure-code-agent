import pytest
from src.main import app

@pytest.fixture
def client():
    # This creates a test client for our Flask app
    with app.test_client() as client:
        yield client

def test_home_route_404(client):
    """Test that the home route returns 404 (since we only have /audit)"""
    response = client.get('/')
    assert response.status_code == 404

def test_audit_route_exists(client):
    """Test that the /audit route accepts POST requests"""
    # We send an empty payload just to check if the route is alive
    response = client.post('/audit', json={"code": "import os"})
    assert response.status_code != 404