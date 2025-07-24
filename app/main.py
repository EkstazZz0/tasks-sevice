from fastapi import FastAPI

from app.core.utils import app_lifespan
from app.endpoints.tasks import router as task_router

app = FastAPI(lifespan=app_lifespan)
app.include_router(task_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
