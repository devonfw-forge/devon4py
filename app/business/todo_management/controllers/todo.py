import logging

from fastapi import APIRouter, Depends

from app.business.todo_management.models.todo import PendingTodosResponse, TodoDto, CreateTodoRequest
from app.business.todo_management.services.todo import TodoService

router = APIRouter(prefix="/todo")

logger = logging.getLogger(__name__)


@router.get("/pending", description="Gets all pending TODOs", response_model=PendingTodosResponse)
async def get_pending_todos(todo_service: TodoService = Depends(TodoService)):
    logger.info("Retrieving all the pending TODOs")
    todos = await todo_service.get_pending_todos()
    return PendingTodosResponse(todos=todos)


@router.post("/create", description="Creates a new TODO", response_model=TodoDto)
async def create_todo(create_request: CreateTodoRequest, todo_service=Depends(TodoService)):
    logger.info("Creating a new TODO")
    todo = await todo_service.create_todo(create_request)
    return todo


@router.get("/subscribe")
async def subscribe(todo_service: TodoService = Depends(TodoService)):
    return todo_service.add_sse()
