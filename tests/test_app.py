import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_normal_input():
    """测试正常输入"""
    response = client.post("/predict", params={"trip_distance": 2.5, "hour": 14, "weekday": 2})
    assert response.status_code == 200
    data = response.json()
    assert "predicted_duration_seconds" in data
    assert data["predicted_duration_seconds"] > 0

def test_zero_distance_edge():
    """边界测试：距离为0"""
    response = client.post("/predict", params={"trip_distance": 0, "hour": 10, "weekday": 1})
    assert response.status_code == 200

def test_late_night_weekend_edge():
    """边界测试：深夜+周末"""
    response = client.post("/predict", params={"trip_distance": 5.0, "hour": 23, "weekday": 6})
    assert response.status_code == 200
    assert response.json()["predicted_duration_seconds"] > 0
