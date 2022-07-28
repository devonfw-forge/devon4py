from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseSettings

from app.common.core.identity_provider import IdentityProvider
from app.common.core.configuration import load_env_file_on_settings


class KeycloakSettings(BaseSettings):
    auth_server: str
    client_id: str
    client_secret: str
    admin_client_secret: str
    realm: str
    callback_uri: str

    class Config:
        env_prefix = "KEYCLOAK_"
        env_file = "TEST.env"


@lru_cache()
def get_keycloak_settings() -> KeycloakSettings:
    return load_env_file_on_settings(KeycloakSettings)


class KeycloakService(IdentityProvider):
    def __init__(self, keycloak_settings: KeycloakSettings):
        from fastapi_keycloak import FastAPIKeycloak
        self._client = FastAPIKeycloak(server_url=keycloak_settings.auth_server,
                                       client_id=keycloak_settings.client_id,
                                       client_secret=keycloak_settings.client_secret,
                                       admin_client_secret=keycloak_settings.admin_client_secret,
                                       realm=keycloak_settings.realm,
                                       callback_uri=keycloak_settings.callback_uri)

    def get_current_user(self, required_roles: list[str] | None = None):
        return self.client.get_current_user(required_roles=required_roles)  # TODO: Refactor to return User

    def configure_api(self, api: FastAPI):
        # Enable authentication layer to swagger endpoints
        self.client.add_swagger_config(api)
        # Include auth router
        from app.common.controllers import keycloak_routers
        api.include_router(keycloak_routers)

    @property
    def client(self):
        return self._client
