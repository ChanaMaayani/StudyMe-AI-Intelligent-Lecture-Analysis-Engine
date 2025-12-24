from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_endpoint_exists():
    """Test that the server is running and responds"""
    response = client.get("/")
    # Accept either 200 (if we have a root endpoint) or 404 (if we don't)
    assert response.status_code in [200, 404]

def test_analyze_endpoint_exists():
    """Test that the analyze endpoint exists"""
    # Test with no file (should return 422 for missing file)
    response = client.post("/analyze")
    assert response.status_code == 422
