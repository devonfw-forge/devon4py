import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.business.todo_management.services.todo import TodoService

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/todos")

logger = logging.getLogger(__name__)


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse('todo/index.html', {"request": request})


@router.get("/pending")
async def pending_todos(request: Request, todo_service: TodoService = Depends(TodoService)):
    todos = await todo_service.get_pending_todos()
    return templates.TemplateResponse('todo/partials/todo_list.html',
                                      {"request": request, "todos": todos})


@router.post("/add")
async def todo_add(description: str = Form(...), todo_service: TodoService = Depends(TodoService)):
    await todo_service.create_todo(description)
    return RedirectResponse(url="/todos/pending", status_code=302)


@router.post("/done/{todo_id}")
async def todo_done(todo_id: uuid.UUID, todo_service: TodoService = Depends(TodoService)):
    await todo_service.todo_done(todo_id)
    return RedirectResponse(url="/todos/pending", status_code=302)
