from sqlmodel import Field
from typing import Optional
from uuid import UUID

from app.common.base.base_entity import BaseUUIDModel


class LinkGroupUser(BaseUUIDModel, table=True):
    group_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="group.id", primary_key=True)
    user_id: Optional[UUID] = Field(default=None, nullable=False, foreign_key="user.id", primary_key=True)
