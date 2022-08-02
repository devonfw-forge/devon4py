from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseSettings

from app.common.core.configuration import load_env_file_on_settings
from app.common.core.identity_provider import IdentityProvider, User
from app.common.exceptions.http import BearerAuthenticationNeededException, InvalidFirebaseAuthenticationException, \
    UnauthorizedException


class FirebaseSettings(BaseSettings):
    credentials_file: str

    class Config:
        env_prefix = "FIREBASE_"
        env_file = "TEST.env"


@lru_cache
def get_firebase_settings() -> FirebaseSettings:
    return load_env_file_on_settings(FirebaseSettings)


class FirebaseService(IdentityProvider):
    def __init__(self, settings: FirebaseSettings):
        import firebase_admin
        firebase_credentials = firebase_admin.credentials.Certificate(settings.credentials_file)  # TODO Refactor to GC library
        self._client = firebase_admin.initialize_app(credential=firebase_credentials)

    def get_current_user(self, required_roles: list[str] | None = None):
        from firebase_admin import auth

        def validate_token(credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> User:
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
            user: User = User(uid=decoded_token['uid'], email=decoded_token['email'], roles=roles)
            return user

        return validate_token

    @property
    def client(self):
        return self._client

    def configure_api(self, api: FastAPI):
        # Include auth router
        from app.common.controllers import firebase_routers
        api.include_router(firebase_routers)
