# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_task_integration():
    response = client.post("/tasks?task_text=Integration test task")
    
    assert response.status_code == 201
    data = response.json()
    assert data["task_text"] == "Integration test task"
    assert "task_id" in data
    
    get_response = client.get(f"/tasks/{data['task_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["task_text"] == "Integration test task"