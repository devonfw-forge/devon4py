import json
from functools import lru_cache
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseSettings

from app.common.core.configuration import load_env_file_on_settings
from app.common.core.identity_provider import IdentityProvider, User
from app.common.exceptions.http import BearerAuthenticationNeededException, InvalidFirebaseAuthenticationException, \
    UnauthorizedException


class FirebaseAuthenticatedUser(User):
    picture: Optional[str]
    name: Optional[str]


class FirebaseSettings(BaseSettings):
    credentials_file: str
    api_key: str

    class Config:
        env_prefix = "FIREBASE_"
        env_file = "TEST.env"


@lru_cache
def get_account_info():
    with open(get_firebase_settings().credentials_file) as f:
        return json.load(f)


@lru_cache
def get_firebase_settings() -> FirebaseSettings:
    return load_env_file_on_settings(FirebaseSettings)


class FirebaseService(IdentityProvider):
    def __init__(self, settings: FirebaseSettings):
        import firebase_admin
        firebase_credentials = firebase_admin.credentials.Certificate(settings.credentials_file)
        self._client = firebase_admin.initialize_app(credential=firebase_credentials)

    def get_current_user(self, required_roles: list[str] | None = None):
        from firebase_admin import auth

        def validate_token(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)))\
                -> FirebaseAuthenticatedUser:
            if credential is None:
                raise BearerAuthenticationNeededException()
            try:
                decoded_token = auth.verify_id_token(credential.credentials, self.client)
            except Exception as err:
                raise InvalidFirebaseAuthenticationException(error=err)
            roles = []
            if 'roles' in decoded_token.keys():
                roles = decoded_token['roles']
            if required_roles is not None:
                for r in required_roles:
                    if r not in roles:
                        raise UnauthorizedException(required_roles)
            user: FirebaseAuthenticatedUser = FirebaseAuthenticatedUser(
                uid=decoded_token["uid"],
                email=decoded_token.get("email", ""),
                roles=roles,
                phone=decoded_token.get("phone", None),
                name=decoded_token.get("name", None),
                picture=decoded_token.get("picture", None)
            )
            return user

        return validate_token

    @property
    def client(self):
        return self._client

    def configure_api(self, api: FastAPI):
        # Include auth router
        from app.common.infra.gcp.controllers import auth_router
        api.include_router(auth_router)
