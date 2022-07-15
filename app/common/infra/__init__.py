from enum import Enum

from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak

from app.common.infra.keycloak import KeycloakSettings, get_keycloak_settings, configure_keycloak_api


class IDPType(Enum):
    KEYCLOAK = 0


def get_idp(keycloak_settings: KeycloakSettings | None):
    # Check if configuration is defined to use Keycloak IDP
    if keycloak_settings is None or keycloak_settings.auth_server is None or keycloak_settings.realm is None:
        return None, None
    else:
        try:
            # Configure Keycloak Authentication
            idp_local = FastAPIKeycloak(
                server_url=keycloak_settings.auth_server,
                client_id=keycloak_settings.client_id,
                client_secret=keycloak_settings.client_secret,
                admin_client_secret=keycloak_settings.admin_client_secret,
                realm=keycloak_settings.realm,
                callback_uri=keycloak_settings.callback_uri
            )
            return idp_local, IDPType.KEYCLOAK
        except Exception:
            # If Keycloak not available return None to disable
            return None, None


idp, idp_type = get_idp(keycloak_settings=get_keycloak_settings())


def configure_api(api: FastAPI):
    if idp_type == IDPType.KEYCLOAK:
        configure_keycloak_api(api)
