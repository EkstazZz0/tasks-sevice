import os

from fastapi import FastAPI

from app.core.config import app_env
from app.db.repository import init_db
from app.db.session import engine


async def app_lifespan(app: FastAPI):
    await init_db()
    yield
    if app_env == "test":
        await engine.dispose()
        os.unlink("./test.db")
