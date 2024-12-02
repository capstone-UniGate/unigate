from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import (
    Session,  # type: ignore
    SQLModel,  # type: ignore  # noqa: F401
    create_engine,
    text,  # type: ignore  # noqa: F401
)

import unigate.models  # type: ignore  # noqa: F401
from unigate.core.config import settings

# make sure all SQLModel models are imported (unigate.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly

engine = create_engine(str(settings.UNIGATE_DB_URI))
auth_engine = create_engine(str(settings.AUTH_DB_URI))


def init_db() -> None:
    # tables should be created with Alembic migrations
    # if you don't use migrations, you can create them here

    # this works because the models are already imported and registered from app.models

    # with Session(engine) as session:
    #     session.execute(text("DROP TYPE IF EXISTS group_type CASCADE;"))  # type: ignore
    #     session.execute(text("DROP TYPE IF EXISTS request_status CASCADE;"))  # type: ignore
    #     session.commit()
    # SQLModel.metadata.drop_all(engine)
    # SQLModel.metadata.create_all(engine)

    pass


def get_session(engine: Engine = engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_auth_session() -> Generator[Session, None, None]:
    return get_session(auth_engine)
