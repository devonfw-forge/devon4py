from typing import Optional
import uuid as uuid_pkg

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime

from app.common.utils import get_current_time


def new_uuid() -> uuid_pkg.UUID:
    # Note: Work around UUIDs with leading zeros: https://github.com/tiangolo/sqlmodel/issues/25
    # by making sure uuid str does not start with a leading 0
    val = uuid_pkg.uuid4()
    while val.hex[0] == '0':
        val = uuid_pkg.uuid4()
    return val


class BaseUUIDModel(SQLModel):
    id: uuid_pkg.UUID = Field(
        default_factory=new_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(default_factory=get_current_time)
    created_at: Optional[datetime] = Field(default_factory=get_current_time)


class BaseCamelModel(BaseModel):
    class Config:
        @classmethod
        def alias_generator(cls, string: str) -> str:
            return ''.join([string.split('_')[0].lower()] + [word.capitalize() for word in string.split('_')[1:]])
