from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field
from app.common.base.base_entity import BaseUUIDModel


# DB ENTITY
class Employee(BaseUUIDModel, table=True):
    name: Optional[str] = Field(nullable=True)
    surname: Optional[str] = Field(nullable=True)
    mail: EmailStr = Field(nullable=False, index=True, sa_column_kwargs={"unique": True})
