import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.business.todo_management.services.todo import TodoService

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/todo")

logger = logging.getLogger(__name__)


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse('todo/index.html', {"request": request})

@router.get("/pending")
async def pending_todos(request: Request, todo_service: TodoService = Depends(TodoService)):
    logger.info("Retrieving all the pending TODOs")
    todos = await todo_service.get_pending_todos()
    return templates.TemplateResponse('todo/partials/todo_list.html',
                                      {"request": request, "todos": todos})
