from sqlmodel import SQLModel, Field
from uuid import UUID

from app.core.enums import TaskStatus

class TaskCreate(SQLModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=3000)
    status: TaskStatus | None = Field(default=TaskStatus.pending)


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=3000)
    status: TaskStatus | None = Field(default=None)
