# db.py
from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine


def get_engine():
    sqlite_url = "sqlite:///database.db"
    return create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    return Session(get_engine())
