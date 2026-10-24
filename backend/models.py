# SQLalchemy tables

from __future__ import annotations
from typing import Annotated, Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import UTC, datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"

class Schedule(Base):
    __tablename__ = "schedule"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task:Mapped[str] = mapped_column(String)
    start_time:Mapped[datetime] = mapped_column(DateTime)
    end_time:Mapped[datetime] = mapped_column(DateTime)
    duration:Mapped[float] = mapped_column(Float)
    task_suggestion:Mapped[Optional[str]] = mapped_column(String)
    is_completed:Mapped[bool] = mapped_column(Boolean, default=False)
