from typing import List

from fastapi import Depends

from app.business.todo_management.models.todo import TodoDto, CreateTodoRequest, TodoID
from app.domain.todo_management.models import Todo
from app.domain.todo_management.repositories.todo import TodoSQLRepository, get_todo_repository as TodoRepository


def parse_to_dto(todo_entity: Todo):
    return TodoDto(**todo_entity.dict())


class TodoService:
    def __init__(self, repository: TodoSQLRepository = Depends(TodoRepository)):
        self.todo_repo = repository

    def get_pending_todos(self) -> List[TodoDto]:
        raw_todos = self.todo_repo.get_pending_todos()
        todo_dtos = map(parse_to_dto, raw_todos)
        return list(todo_dtos)

    def create_todo(self, create_req: CreateTodoRequest) -> TodoDto:
        raw_new_todo = self.todo_repo.create(description=create_req.description)
        return parse_to_dto(raw_new_todo)

    def todo_done(self, todo: TodoID):
        self.todo_repo.todo_done(todo_id=todo.id)
