from typing import List
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
