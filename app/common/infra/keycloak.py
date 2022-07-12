from functools import lru_cache
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseSettings

from app.common.core.configuration import __load_env_file_on_settings


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


@lru_cache()
def get_keycloak_settings() -> KeycloakSettings:
    return __load_env_file_on_settings(KeycloakSettings)


def configure_keycloak_api(api: FastAPI):
    from app.common import idp
    if idp is not None:
        # Enable authentication layer to swagger endpoints
        idp.add_swagger_config(api)
        # Include auth router
        from app.common.controllers import auth_router
        api.include_router(auth_router)
