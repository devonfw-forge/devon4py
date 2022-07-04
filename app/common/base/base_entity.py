from typing import Optional
import uuid as uuid_pkg
from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseUUIDModel(SQLModel):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
