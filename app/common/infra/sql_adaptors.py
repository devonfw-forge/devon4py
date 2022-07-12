from functools import lru_cache
from typing import Optional

from fastapi import Depends
from pydantic import BaseSettings
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, SQLModel, create_engine

from app.common.core.configuration import __load_env_file_on_settings


class DatabaseSettings(BaseSettings):
    type: str
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int] = None
    database: Optional[str]
    enable_logs = False
    pool_size = 5

    class Config:
        env_prefix = "DB_"
        env_file = "TEST.env"


@lru_cache()
def get_db_settings() -> DatabaseSettings:
    return __load_env_file_on_settings(DatabaseSettings)


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
    return create_engine(db_uri, echo=settings.enable_logs, echo_pool=settings.enable_logs, pool_pre_ping=True,
                         connect_args={"check_same_thread": False})


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
