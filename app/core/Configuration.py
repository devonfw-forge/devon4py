from typing import Optional, Type, Generic, Union, List

import yaml
from fastapi import FastAPI
from pydantic import BaseSettings, AnyHttpUrl, validator
import os
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware


class GlobalSettings(BaseSettings):
    app_name: str = "My Awesome API"
    environment: str = "TEST"
    port: int = 80
    swagger_path: str = "/docs"
    cors: List[str] | List[AnyHttpUrl] = []

    @validator("cors", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if v is None:
            print("CORS Not Specified")
            return []
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

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
    pool_size = 5

    class Config:
        env_prefix = "DB_"
        env_file = "TEST.env"


def __load_env_file_on_settings(settings: Type[BaseSettings]):
    env = os.environ.get("ENV")
    if env:
        return settings(_env_file="{}.env".format(env))
    else:
        return settings()


@lru_cache()
def get_global_settings() -> GlobalSettings:
    return __load_env_file_on_settings(GlobalSettings)


@lru_cache()
def get_db_settings() -> DatabaseSettings:
    return __load_env_file_on_settings(DatabaseSettings)


@lru_cache()
def get_log_config():
    with open("logging.yaml") as logconf:
        log_config = yaml.safe_load(logconf)
        return log_config


def get_api():
    app_settings = get_global_settings()
    from app.controllers import api_router
    api = FastAPI(docs_url=app_settings.swagger_path, title=app_settings.app_name)
    # Set all CORS enabled origins
    if app_settings.cors and len(app_settings.cors) > 0:
        api.add_middleware(
            CORSMiddleware,
            allow_origins=app_settings.cors,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"]
        )
    api.include_router(api_router)
    return api
