from sqlmodel import Field
from app.common.base.base_entity import BaseUUIDModel


# DB ENTITY
class Todo(BaseUUIDModel, table=True):
    description: str = Field(nullable=False)
    done: bool = Field(nullable=False, default=False)
