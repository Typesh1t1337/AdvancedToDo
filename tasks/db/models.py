from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class Permission(enum.Enum):
    read = "read"
    write = "write"


class Status(enum.Enum):
    active = "active"
    inactive = "inactive"


class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, index=True, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority), index=True, nullable=True)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.active, nullable=False)
    category: Mapped[str] = mapped_column(String, index=True, nullable=True)
    repeat_rule: Mapped[str] = mapped_column(String, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    shared_tasks = relationship("SharedTask", back_populates="task")


class SharedTask(Base):
    __tablename__ = 'shared_tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    shared_with_user_id: Mapped[int] = mapped_column(Integer, index=True)
    permission: Mapped[Permission] = mapped_column(Enum(Permission), index=True, default=Permission.read, nullable=False)

    task = relationship("Task", back_populates="shared_tasks")
