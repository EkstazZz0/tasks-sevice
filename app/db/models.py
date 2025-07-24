from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from app.core.enums import TaskStatus


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(min_length=3, max_length=150)
    description: str | None = Field(default=None, nullable=True, max_length=3000)
    status: TaskStatus | None = Field(default=TaskStatus.pending)
    created_at: datetime = Field(default_factory=datetime.now)
