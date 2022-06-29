from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from app.domain.models.links import LinkGroupUser
from app.common.base.base_entity import BaseUUIDModel
from uuid import UUID

from app.domain.models.user import User


class GroupBase(SQLModel):
    name: str
    description: str


class Group(BaseUUIDModel, GroupBase, table=True):
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy":"selectin", "primaryjoin":"Group.created_by_id==User.id"})
    users: List["User"] = Relationship(back_populates="groups", link_model=LinkGroupUser, sa_relationship_kwargs={"lazy": "selectin"})
