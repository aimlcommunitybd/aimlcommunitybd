"""Database utilities for SQLModel with SQLite."""

from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager

import os
from dotenv import load_dotenv

load_dotenv()
debug_mode = os.getenv("DEBUG", "False").lower() == "true"
_engine = None


def get_engine():
    """Get or create singleton SQLite database engine."""
    global _engine
    if _engine is None:
        sqlite_url = "sqlite:///database.db"
        _engine = create_engine(sqlite_url, echo=debug_mode)
    return _engine


def init_db():
    """Create all database tables from SQLModel definitions."""
    SQLModel.metadata.create_all(get_engine())


def get_session_raw():
    """Create new database session. Must be manually closed after use."""
    return Session(get_engine())


@contextmanager
def get_session():
    """Create database session with automatic cleanup."""
    session = Session(get_engine())
    try:
        yield session
        # session.commit()
    except Exception:
        # session.rollback()
        raise
    finally:
        session.close()
