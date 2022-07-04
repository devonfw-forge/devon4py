from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session

from .configuration import DatabaseSettings, get_db_settings


def get_db_uri(db_settings: DatabaseSettings = Depends(get_db_settings)) -> str:
    if db_settings.type == "LOCAL":
        uri = "sqlite:///{}.db".format(db_settings.database)
    elif db_settings.type == "PG":
        uri = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            db_settings.username, db_settings.password, db_settings.host, db_settings.port, db_settings.database)
    else:
        uri = "sqlite:///database.db"
    return uri


def get_async_db_uri(db_settings: DatabaseSettings = Depends(get_db_settings)) -> str:
    if db_settings.type == "LOCAL":
        uri = "sqlite+aiosqlite:///{}.db".format(db_settings.database)
    elif db_settings.type == "PG":
        uri = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            db_settings.username, db_settings.password, db_settings.host, db_settings.port, db_settings.database)
    else:
        uri = "sqlite+aiosqlite:///database.db"
    return uri


def get_db_engine(settings: DatabaseSettings = Depends(get_db_settings), db_uri: str = Depends(get_db_uri)) -> Engine:
    return create_engine(db_uri, echo=settings.enable_logs, echo_pool=settings.enable_logs, pool_pre_ping=True)


def get_async_db_engine(settings: DatabaseSettings = Depends(get_db_settings), db_uri: str = Depends(get_async_db_uri)):
    return create_async_engine(db_uri,
                               echo=settings.enable_logs, echo_pool=settings.enable_logs,
                               future=True, pool_pre_ping=True)


def get_session(engine: Engine = Depends(get_db_engine)):
    sess = None
    try:
        sess = Session(engine)
        yield sess
    finally:
        if sess:
            sess.close()


def init_db_entities(db: DatabaseSettings):
    engine = get_db_engine(db, get_db_uri(db))
    SQLModel.metadata.create_all(engine)

#
# def get_db_session_factory(engine: Engine = Depends(get_async_db_engine)):
#     """
#         Generates a session factory from the configured SQL Engine
#     """
#     return sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)

#
# def get_db(session_factory: sessionmaker = Depends(get_session_factory)) -> Generator:
#     """
#         Generates a database session from the configured factory // TODO: Problem with async close
#     """
#     try:
#         db = session_factory()
#         yield db
#     finally:
#         db.close()
