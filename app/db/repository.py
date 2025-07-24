from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from app.core.enums import TaskStatus
from app.db.models import Task
from app.db.session import engine
from app.schemas.tasks import TaskUpdate


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_task(session: AsyncSession, task_id: UUID) -> Task:
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    return task


async def get_tasks(
    session: AsyncSession, limit: int, offset: int, status: TaskStatus | None = None
) -> list[Task]:
    get_items_statement = select(Task).limit(limit=limit).offset(offset=offset)

    if status:
        get_items_statement = get_items_statement.where(Task.status == status)

    return (await session.execute(get_items_statement)).scalars().all()


async def update_task(
    session: AsyncSession, db_task: Task, update_task_data: TaskUpdate
) -> Task:
    db_task.sqlmodel_update(update_task_data.model_dump(exclude_unset=True))

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task
