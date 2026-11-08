from collections.abc import Iterator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from retain.config import settings


def make_engine(url: str) -> Engine:
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


engine = make_engine(settings.database_url)


def init_db(eng: Engine = engine) -> None:
    # Importing models registers their tables on SQLModel.metadata.
    from retain import models  # noqa: F401

    SQLModel.metadata.create_all(eng)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
