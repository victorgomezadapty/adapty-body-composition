"""Database engine and session management."""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)


def init_db() -> None:
    """Create database tables for all imported SQLModel table models."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependencies."""
    with Session(engine) as session:
        yield session

