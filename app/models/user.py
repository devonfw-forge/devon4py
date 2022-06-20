from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from app.models.links import LinkGroupUser
from typing import List, Optional
from pydantic import EmailStr, BaseModel
from app.models.base import BaseUUIDModel
from uuid import UUID

# DB ENTITY


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(nullable=True, index=True, sa_column_kwargs={"unique": True})
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))  # bday with timezne
    phone: Optional[str]
    state: Optional[str]
    country: Optional[str]
    address: Optional[str]


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str = Field(nullable=False, index=True)
    role_id: Optional[UUID] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "selectin"})
    groups: List["Group"] = Relationship(back_populates="users", link_model=LinkGroupUser,
                                         sa_relationship_kwargs={"lazy": "selectin"})


# REQUESTS

class UserCreateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    email: EmailStr
    is_superuser: bool = False
    role_id: Optional[UUID]


class UserUpdateRequest(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True


# RESPONSES

class UserStatusEnum(str, Enum):
    active = 'active'
    inactive = 'inactive'
