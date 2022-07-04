from typing import Optional, Type, List

import yaml
from fastapi import FastAPI, APIRouter
from fastapi_keycloak import FastAPIKeycloak
from pydantic import BaseSettings, AnyHttpUrl, validator
import os
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware


# Configuration Objects Definitions
from app.common.core.exception_handlers import init_exception_handlers
from app.common.infra.keycloak import get_idp, KeycloakSettings


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


# Utils to load Configurations

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
def get_keycloak_settings() -> KeycloakSettings:
    return __load_env_file_on_settings(KeycloakSettings)


@lru_cache()
def get_log_config():
    with open("logging.yaml") as logconf:
        log_config = yaml.safe_load(logconf)
        return log_config


def get_api(routers: List[APIRouter]):
    app_settings = get_global_settings()
    api = FastAPI(docs_url=app_settings.swagger_path, title=app_settings.app_name)
    idp = get_idp(keycloak_settings=get_keycloak_settings())
    if idp is not None:
        # Enable authentication layer to swagger endpoints
        idp.add_swagger_config(api)
    # Set CORS enabled origins
    if app_settings.cors and len(app_settings.cors) > 0:
        api.add_middleware(
            CORSMiddleware,
            allow_origins=app_settings.cors,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"]
        )
    # Include auth router
    if idp is not None:
        from app.common.controllers import auth_router
        api.include_router(auth_router)
    # Include selected routers
    for r in routers:
        api.include_router(r)
    # Init exception Handlers
    init_exception_handlers(api)
    return api
