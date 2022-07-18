from fastapi import FastAPI

from app.common.core.identity_provider import idp_type, IDPType
from app.common.infra.firebase import FirebaseSettings, get_firebase_settings, FirebaseService
from app.common.infra.keycloak import KeycloakSettings, get_keycloak_settings, configure_keycloak_api, KeycloakService


def configure_api(api: FastAPI):
    if idp_type == IDPType.KEYCLOAK:
        configure_keycloak_api(api)
