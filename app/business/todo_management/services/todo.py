from typing import List

from fastapi import Depends
from sse_starlette import ServerSentEvent

from app.business.todo_management.models.todo import TodoDto, CreateTodoRequest, TodoID
from app.common.services.sse import EventPublisher
from app.domain.todo_management.models import Todo
from app.domain.todo_management.repositories.todo import TodoSQLRepository


def parse_to_dto(todo_entity: Todo):
    return TodoDto(**todo_entity.dict())


class TodoService:
    _todo_event_publisher = EventPublisher()

    def __init__(self, repository: TodoSQLRepository = Depends(TodoSQLRepository)):
        # TODO: Currently EventPublisher is only supported when workers=1
        self.todo_repo = repository

    async def get_pending_todos(self) -> List[TodoDto]:
        raw_todos = await self.todo_repo.get_pending_todos()
        todo_dtos = map(parse_to_dto, raw_todos)
        return list(todo_dtos)

    async def create_todo(self, create_req: CreateTodoRequest) -> TodoDto:
        raw_new_todo = await self.todo_repo.create(description=create_req.description)
        todo_dto = parse_to_dto(raw_new_todo)
        self._notify_todo_added(todo_dto)
        return todo_dto

    def add_sse(self) -> ServerSentEvent:
        _, sse = self._todo_event_publisher.subscribe()
        return sse

    def _notify_todo_added(self, todo):
        # Publish the new to_do as an event on the topic "todo_added"
        self._todo_event_publisher.publish(todo, "todo_added")

    async def todo_done(self, todo: TodoID):
        await self.todo_repo.todo_done(todo_id=todo.id)
