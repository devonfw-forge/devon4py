from typing import Optional
import uuid as uuid_pkg
from sqlmodel import SQLModel, Field
from datetime import datetime


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
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
