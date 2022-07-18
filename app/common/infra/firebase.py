from functools import lru_cache
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseSettings

from app.common.core.configuration import __load_env_file_on_settings
from app.common.exceptions.http import BearerAuthenticationNeededException, InvalidFirebaseAuthenticationException
from app.common.core.identity_provider import IdentityProvider


class FirebaseSettings(BaseSettings):
    credentials_file: Optional[str]
    database_url: Optional[str]

    class Config:
        env_prefix = "FIREBASE_"
        env_file = "TEST.env"


@lru_cache()
def get_firebase_settings() -> FirebaseSettings:
    return __load_env_file_on_settings(FirebaseSettings)


class FirebaseService(IdentityProvider):
    def __init__(self, settings: FirebaseSettings):
        import firebase_admin
        firebase_credentials = firebase_admin.credentials.Certificate(settings.credentials_file)
        options = {}
        if settings.database_url:
            options['databaseURL'] = settings.database_url
        firebase_admin.initialize_app(credential=firebase_credentials, options=options)

    def get_current_user(self, required_roles: list[str] | None = None):
        from firebase_admin import auth

        def validate_token(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
            if credential is None:
                raise BearerAuthenticationNeededException()
            try:
                decoded_token = auth.verify_id_token(credential.credentials)
            except Exception as err:
                raise InvalidFirebaseAuthenticationException(error=err)
            return decoded_token

        return validate_token
