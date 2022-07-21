from typing import Generic, TypeVar, Type, Union, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select

from app.common.exceptions.http import NotFoundException
from app.common.infra.sql_adaptors import get_async_session, AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseSQLRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession = Depends(get_async_session)):
        """
        Object with default methods to Create, Read, Update and Delete (CRUD).
        """
        self.model = model
        self.session = session

    async def get(self, *, uid: Union[UUID, str]) -> Optional[ModelType]:
        response = await self.session.exec(
            select(self.model)
            .where(self.model.id == uid)
            .options(selectinload('*'))
        )
        response = response.one_or_none()
        if not response:
            raise NotFoundException(detail="Not found with ID {}".format(uid))
        return response

    async def add(self, *, model: ModelType):
        await self.save(model=model, refresh=True)

    async def save(self, *, model: ModelType, refresh=False):
        self.session.add(model)
        await self.session.commit()
        if refresh:
            await self.session.refresh(model)
