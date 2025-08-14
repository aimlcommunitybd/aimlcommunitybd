# models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    image_url: str
    title: str
    description: Optional[str]
    youtube_link: Optional[str] = None

    __tablename__ = "activities"
