import pytest
from asgi_lifespan import LifespanManager
from datatest import task_create_data
from httpx import ASGITransport, AsyncClient

from app.db.models import Task
from app.db.session import get_session
from app.main import app


@pytest.fixture()
async def prepared_task():
    session_generator = get_session()
    session = await session_generator.__anext__()
    db_task = Task.model_validate(task_create_data)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    yield db_task
    await session_generator.aclose()


@pytest.fixture()
async def async_client():
    async with LifespanManager(app=app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client
