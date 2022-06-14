from typing import Optional

import yaml
from fastapi import FastAPI
from pydantic import BaseSettings
import os
from functools import lru_cache


class GlobalSettings(BaseSettings):
    app_name: str = "My Awesome API"
    environment: str = "TEST"
    port: int = 80
    swagger_path: str = "docs"

    class Config:
        env_file = "TEST.env"


class DatabaseSettings(BaseSettings):
    type: str
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int] = None
    database: Optional[str]
    enable_logs = False

    class Config:
        env_prefix = "DB_"
        env_file = "TEST.env"


def __load_env_file_on_settings(settings):
    env = os.environ.get("ENV")
    if env:
        return settings(_env_file="{}.env".format(env))
    else:
        return settings()


@lru_cache()
def get_global_settings():
    return __load_env_file_on_settings(GlobalSettings)


@lru_cache()
def get_db_settings():
    return __load_env_file_on_settings(DatabaseSettings)


@lru_cache()
def get_log_config():
    with open("logging.yaml") as logconf:
        log_config = yaml.safe_load(logconf)
        return log_config


def get_app():
    app_settings = get_global_settings()
    app = FastAPI(docs_url=app_settings.swagger_path)
    return app
