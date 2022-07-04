from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import select, Session

from app.common.base.base_repository import BaseRepository
from app.common.core.database import get_session
from app.common.exceptions.http import NotFoundException
from app.domain.models.todo import Todo


class TodoRepository(BaseRepository[Todo]):

    def create(self, *, description: str) -> Todo:
        new_todo = Todo(description=description)
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return new_todo

    def get_pending_todos(self) -> List[Todo]:
        todos = self.session.exec(select(Todo).where(Todo.done == False))
        return todos.all()

    def todo_done(self, todo_id: UUID) -> Todo:
        query = self.session.exec(select(Todo).where(Todo.id == todo_id))
        todo = query.one_or_none()
        if not todo:
            raise NotFoundException(detail="TODO not found with ID {}".format(todo_id))
        todo.done = True
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo


def get_todo_repository(session: Session = Depends(get_session)):
    return TodoRepository(Todo, session)
