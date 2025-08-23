# models.py
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Column
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from typing import Optional
from datetime import datetime


class User(SQLModel, UserMixin, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_admin: bool = False
    active: bool = Field(default=False, alias="is_active")  # Use alias
    created: datetime = Field(default_factory=datetime.now)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ActivityCategory(str, Enum):
    # UPCOMING = "upcoming"
    WEBINAR = "webinar"
    WORKSHOP = "workshop"
    COMPETITION = "competition"
    MEETUP = "meetup"


class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    id: Optional[int] = Field(default=None, primary_key=True)
    category: ActivityCategory = Field(
        default=ActivityCategory.WEBINAR, 
        sa_column=Column(SQLEnum(ActivityCategory))
    )
    image_url: str = Field(default="", max_length=255)
    title: str = Field(default="", max_length=255)
    description: Optional[str] = None
    youtube_link: Optional[str] = None
    event_date: Optional[datetime] = None
    is_upcoming: Optional[bool] = True
    created: datetime = Field(default_factory=datetime.now)
