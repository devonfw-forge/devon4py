from typing import Optional, Type, Generic, Union, List

import yaml
from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak
from pydantic import BaseSettings, AnyHttpUrl, validator
import os
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware


# Configuration Objects Definitions

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


class KeycloakSettings(BaseSettings):
    auth_server: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    admin_client_secret: Optional[str]
    realm: Optional[str]
    callback_uri: Optional[str]

    class Config:
        env_prefix = "KEYCLOAK_"
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


def get_idp():
    print("Init Keycloak")
    keycloak_settings = get_keycloak_settings()
    # Check if configuration is defined to use Keycloak IDP
    if keycloak_settings.auth_server is None or keycloak_settings.realm is None:
        return None
    # Configure Keycloak Authentication
    idp = FastAPIKeycloak(
        server_url=keycloak_settings.auth_server,
        client_id=keycloak_settings.client_id,
        client_secret=keycloak_settings.client_secret,
        admin_client_secret=keycloak_settings.admin_client_secret,
        realm=keycloak_settings.realm,
        callback_uri=keycloak_settings.callback_uri
    )
    return idp


def get_api():
    app_settings = get_global_settings()
    api = FastAPI(docs_url=app_settings.swagger_path, title=app_settings.app_name)
    idp = get_idp()
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
    # Include all Routers
    from app.controllers import api_router
    api.include_router(api_router)
    return api
