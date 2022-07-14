import logging

from fastapi import APIRouter, Depends

from app.business.todo_management.models.todo import PendingTodosResponse, TodoDto, CreateTodoRequest
from app.business.todo_management.services.todo import TodoService

router = APIRouter(prefix="/todo")

logger = logging.getLogger(__name__)


@router.get("/pending", description="Gets all pending TODOs", response_model=PendingTodosResponse)
def get_pending_todos(todo_service: TodoService = Depends(TodoService)):
    logger.info("Retrieving all the pending TODOs")
    todos = todo_service.get_pending_todos()
    return PendingTodosResponse(todos=todos)


@router.post("/create", description="Creates a new TODO", response_model=TodoDto)
def create_todo(create_request: CreateTodoRequest, todo_service: TodoService = Depends(TodoService)):
    logger.info("Creating a new TODO")
    todo = todo_service.create_todo(create_request)
    return todo
