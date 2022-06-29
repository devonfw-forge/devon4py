from typing import Generic, TypeVar, Type, Union, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload, sessionmaker
from sqlmodel import SQLModel

from app.common.core.database import get_db_session_factory

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: sessionmaker = Depends(get_db_session_factory)):
        """
        Object with default methods to Create, Read, Update and Delete (CRUD).
        """
        self.model = model
        self.create_session = session

    async def get(self, *, id: Union[UUID, str]) -> Optional[ModelType]:
        async with self.create_session() as db_session:
            response = await db_session.exec(
                select(self.model)
                .where(self.model.id == id)
                .options(selectinload('*'))
            )
            return response.first()
