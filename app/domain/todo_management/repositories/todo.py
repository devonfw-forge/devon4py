from typing import List
from uuid import UUID

from fastapi import Depends
from sqlmodel import select, Session

from app.common.base.base_repository import BaseSQLRepository
from app.common.exceptions.http import NotFoundException
from app.common.infra.sql_adaptors import get_session
from app.domain.todo_management.models import Todo


class TodoSQLRepository(BaseSQLRepository[Todo]):

    def create(self, *, description: str) -> Todo:
        new_todo = Todo(description=description)
        self.add(model=new_todo)
        return new_todo

    def get_pending_todos(self) -> List[Todo]:
        todos = self.session.exec(select(Todo).where(Todo.done == False))
        return todos.all()

    def todo_done(self, todo_id: UUID) -> Todo:
        todo = self.get(uid=todo_id)
        todo.done = True
        self.save(model=todo, refresh=False)
        return todo


def get_todo_repository(session: Session = Depends(get_session)):
    return TodoSQLRepository(Todo, session)
