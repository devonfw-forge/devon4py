import asyncio
import datetime
import functools
import json
import mimetypes
from functools import lru_cache
from typing import BinaryIO, ParamSpec, TypeVar, Callable, Awaitable

from google.cloud.storage import Client, Bucket
from pydantic import BaseSettings

from app.common.core.configuration import load_env_file_on_settings
from app.common.infra.gcp.firebase import get_account_info
from app.domain.todo_management.utils import get_current_time


class BaseStorageSettings(BaseSettings):
    credentials_file: str
    bucket: str
    expiration_time: int

    class Config:
        env_prefix = "STORAGE_"
        env_file = "TEST.env"


@lru_cache
def get_storage_settings() -> BaseStorageSettings:
    return load_env_file_on_settings(BaseStorageSettings)


_storage_client: Client | None = None


def _get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = Client.from_service_account_info(get_account_info())
    return _storage_client


P = ParamSpec("P")
R = TypeVar("R")


def run_in_executor(f: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def async_f(*args: P.args, **kwargs: P.kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor=None,
            func=functools.partial(f, *args, **kwargs)
        )

    return async_f


class CloudStorage:
    def __init__(self,
                 client: Client,
                 storage_config: BaseStorageSettings):
        self._client = client
        self._configuration = storage_config

    def _bucket(self) -> Bucket:
        return self._client.bucket(self._configuration.bucket)

    @run_in_executor
    def _upload_file(self, *, path: str, filename: str, data: BinaryIO | bytes) -> str:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        path = f"{path}/{filename}"
        blob = self._bucket().blob(path)
        if isinstance(data, bytes):
            blob.upload_from_string(data, content_type=content_type)
        else:
            blob.upload_from_file(data, content_type=content_type)
        return blob.name

    async def upload_file(self, *, path: str, filename: str, data: BinaryIO | bytes) -> str:
        return await self._upload_file(path=path, filename=filename, data=data)

    def generate_signed_url(self, reference: str | None):
        if reference:
            return self._bucket().blob(reference).generate_signed_url(expiration=self._expiration_time())
        else:
            return None

    def _expiration_time(self) -> datetime.datetime:
        return get_current_time() + datetime.timedelta(seconds=self._configuration.expiration_time)

    @run_in_executor
    def _delete(self, reference: str | None = None, prefix: str | None = None):
        if reference:
            blob_iterator = [self._bucket().blob(reference)]
        elif prefix:
            blob_iterator = self._client.list_blobs(self._bucket(), prefix=prefix)
        else:
            raise ValueError("Either reference or prefix must be defined")

        for blob in blob_iterator:
            blob.delete()

    async def delete(self, reference: str | None = None, prefix: str | None = None):
        await self._delete(reference, prefix)
