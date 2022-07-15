from typing import List
from uuid import UUID

from fastapi import Depends
from sqlmodel.sql.expression import Select, select

from app.common.base.base_repository import BaseSQLRepository
from app.common.exceptions.http import NotFoundException
from app.common.infra.sql_adaptors import get_session, get_async_session, AsyncSession
from app.domain.todo_management.models import Todo


class TodoSQLRepository(BaseSQLRepository[Todo]):

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(Todo, session)

    async def create(self, *, description: str) -> Todo:
        new_todo = Todo(description=description)
        await self.add(model=new_todo)
        return new_todo

    async def get_pending_todos(self) -> List[Todo]:
        todos = await self.session.exec(select(Todo).where(Todo.done == False))
        return todos.all()

    async def todo_done(self, todo_id: UUID) -> Todo:
        todo = await self.get(uid=todo_id)
        todo.done = True
        await self.save(model=todo, refresh=False)
        return todo
