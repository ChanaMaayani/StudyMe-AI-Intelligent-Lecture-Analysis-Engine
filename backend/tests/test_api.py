import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_analyze_requires_file():
    response = client.post("/analyze")
    assert response.status_code == 422
