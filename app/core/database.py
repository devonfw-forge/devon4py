from functools import lru_cache

from fastapi import Depends
from sqlalchemy.future import Engine

from .configuration import DatabaseSettings, get_db_settings
from sqlmodel import Field, Session, SQLModel, create_engine


def get_db_engine(db: DatabaseSettings = Depends(get_db_settings)) -> Engine:
    if db.type == "LOCAL":
        engine = create_engine("sqlite:///{}.db".format(db.database), echo=db.enable_logs, echo_pool=db.enable_logs)
    elif db.type == "PG":
        engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            db.username, db.password, db.host, db.port, db.database), echo=db.enable_logs, echo_pool=db.enable_logs)
    else:
        engine = create_engine("sqlite:///database.db")
    return engine


def init_db_entities(db: DatabaseSettings):
    import app.models
    engine = get_db_engine(db)
    SQLModel.metadata.create_all(engine)

