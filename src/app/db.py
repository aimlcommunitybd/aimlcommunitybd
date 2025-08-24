"""Database utilities for SQLModel with SQLite."""
import os
from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from dotenv import load_dotenv

from app import settings

load_dotenv()

debug_mode = settings.DEBUG
_engine = None


def get_engine():
    """Get or create singleton SQLite database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.DATABASE_URL, echo=debug_mode
        )
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
