from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine  # noqa: F401

from unigate.core.config import settings
from unigate.models import Group, Join, Request, Student, SuperStudent  # noqa: F401

# Use the settings to configure the engine
engine = create_engine(str(settings.DATABASE_URI))


def get_session() -> Generator[Session, None, None]:
    """Create and return a new session."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
