from typing import List, Any
from uuid import UUID

from pydantic import BaseModel


class TodoID(BaseModel):
    id: UUID


class CreateTodoRequest(BaseModel):
    description: str


class TodoDto(TodoID, CreateTodoRequest):
    done: bool


class PendingTodosResponse(BaseModel):
    todos: List[TodoDto]


class EventPublishRequest(BaseModel):
    data: Any
    event: None | str
