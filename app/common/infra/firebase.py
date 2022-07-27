from functools import lru_cache
from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseSettings, ValidationError

from app.common.core.configuration import load_env_file_on_settings
from app.common.exceptions.http import BearerAuthenticationNeededException, InvalidFirebaseAuthenticationException, \
    UnauthorizedException
from app.common.core.identity_provider import IdentityProvider, User
import asyncio
from typing import TypeVar, Generic, Type, Callable
from google.cloud.firestore_v1 import AsyncClient, AsyncDocumentReference, AsyncCollectionReference
from google.cloud.firestore_v1.base_document import BaseDocumentReference
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pydantic import BaseModel


class FirebaseSettings(BaseSettings):
    credentials_file: str

    class Config:
        env_prefix = "FIREBASE_"
        env_file = "TEST.env"


@lru_cache()
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



class BaseFirebaseModel(BaseModel):
    document_id: str

    class Config:
        #Temporary solution. Need to create validators for references
        arbitrary_types_allowed = True


ModelType = TypeVar("ModelType", bound=BaseFirebaseModel)


class Location(BaseFirebaseModel):
    # TODO
    pass


class UserModel(BaseFirebaseModel):
    trusted_users: list[str]
    location: BaseDocumentReference
    do_not_disturb: bool


class BaseFirestoreRepository(Generic[ModelType]):
    def __init__(self, *, collection_path: str | tuple[str], model: Type[ModelType], client: AsyncClient):
        """
        Object with default methods to Create, Read, Update and Delete (CRUD) from a Firestore Collection.
        """
        self._client = client
        self._model = model
        self._path = collection_path if isinstance(collection_path, tuple) else tuple(collection_path.split("/"))

    def _get_collection_reference(self) -> AsyncCollectionReference:
        return self._client.collection(*self._path)

    def _get_document_reference(self, document_id: str) -> AsyncDocumentReference:
        return self._client.document(*self._path, document_id)

    async def get(self, document_id: str) -> ModelType | None:
        snapshot = await self._get_document_reference(document_id).get()
        return self._model(document_id=snapshot.id, **snapshot.to_dict()) if snapshot.exists else None

    def add_callback(self, document_id: str, callback = Callable):
        # TODO: Async client does not implement on_snapshot, we need to use the sync client
        # return self._get_document_reference(document_id).on_snapshot(callback)
        raise NotImplementedError

    async def add(self, *, model: ModelType):
        ...

    async def save(self, *, model: ModelType, refresh=False):
        ...


class UsersRepo(BaseFirestoreRepository[UserModel]):
    pass


async def print_users(async_client: AsyncClient):
    users_collection = async_client.collection("users")
    users = users_collection.list_documents()
    async for user_reference in users:
        user_data = UserModel(**(await user_reference.get()).to_dict())
        print(user_data)


async def print_locations(async_client: AsyncClient):
    locations_collection = async_client.collection("locations")
    async for location in locations_collection.list_documents():
        location_data = (await location.get()).to_dict()
        print(location_data)


async def async_main():
    alice = await users_repo.get("alice")
    print(alice)


if __name__ == '__main__':
    credentials: Credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    client = AsyncClient(credentials=credentials)
    users_repo = UsersRepo(collection_path="users", model=UserModel, client=client)
    asyncio.run(async_main())
