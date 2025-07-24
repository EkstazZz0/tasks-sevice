from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.enums import TaskStatus
from app.db.models import Task
from app.db.repository import get_task as db_get_task
from app.db.repository import get_tasks as db_get_tasks
from app.db.repository import update_task as db_update_task
from app.db.session import SessionDep
from app.schemas.tasks import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks")


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(session: SessionDep, task_request: TaskCreate):
    db_task = Task.model_validate(task_request)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.get("", response_model=list[Task])
async def get_tasks(
    session: SessionDep,
    limit: Annotated[int | None, Query(gt=0, le=100)] = 10,
    offset: Annotated[int | None, Query(ge=0)] = 0,
    status: Annotated[TaskStatus | None, Query()] = None,
):
    return await db_get_tasks(
        session=session, limit=limit, offset=offset, status=status
    )


@router.get("/{task_id}", response_model=Task)
async def get_task(session: SessionDep, task_id: UUID):
    return await db_get_task(session=session, task_id=task_id)


@router.put("/{task_id}", response_model=Task)
async def update_task(session: SessionDep, task_id: UUID, update_task_data: TaskUpdate):
    db_task = await db_get_task(session=session, task_id=task_id)
    return await db_update_task(
        session=session, db_task=db_task, update_task_data=update_task_data
    )


@router.delete("/{task_id}")
async def delete_task(session: SessionDep, task_id: UUID):
    db_task = await db_get_task(session=session, task_id=task_id)

    await session.delete(db_task)
    await session.commit()

    return {"success": True, "detail": f"Task with id {task_id} deleted"}
