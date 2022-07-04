from typing import Optional

from fastapi_keycloak import FastAPIKeycloak
from pydantic import BaseSettings


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


def get_idp(keycloak_settings: KeycloakSettings):
    # Check if configuration is defined to use Keycloak IDP
    if keycloak_settings.auth_server is None or keycloak_settings.realm is None:
        return None
    try:
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
    except:
        # If Keycloak not available return None to disable
        return None
