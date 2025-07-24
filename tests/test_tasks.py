from fastapi.testclient import TestClient

from datatest import task_create_data

def test_1_create_task(client: TestClient):
    response = client.post("/tasks", json=task_create_data)
    assert response.status_code
