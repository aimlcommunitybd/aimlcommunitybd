# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    image_url: str
    title: str
    description: Optional[str]
    youtube_link: Optional[str] = None
    event_date: Optional[str] = None
    created: datetime = Field(default=datetime.now())

    __tablename__ = "activities"
