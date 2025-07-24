import pytest
from datatest import task_create_data


@pytest.mark.asyncio
async def test_1_create_task(async_client):
    response = await async_client.post("/tasks", json=task_create_data)

    assert response.status_code == 201

    db_task = response.json()
    db_task.pop("id")
    db_task.pop("created_at")

    assert db_task == task_create_data


@pytest.mark.asyncio
async def test_2_get_tasks(async_client, prepared_task):
    response = await async_client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    print(data)
    task_data = prepared_task.model_dump()
    task_data["created_at"] = task_data["created_at"].isoformat()
    task_data["id"] = str(task_data["id"])
    assert data[0] == task_data
