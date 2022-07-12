from typing import Generic, TypeVar, Type, Union, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, Session

from app.common.infra.sql_adaptors import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseSQLRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: Session = Depends(get_session)):
        """
        Object with default methods to Create, Read, Update and Delete (CRUD).
        """
        self.model = model
        self.session = session

    def get(self, *, uid: Union[UUID, str]) -> Optional[ModelType]:
        response = self.session.exec(
            select(self.model)
            .where(self.model.id == uid)
            .options(selectinload('*'))
        )
        return response.one_or_none()
