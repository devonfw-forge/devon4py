from fastapi import APIRouter
# Include all routers here
from app.business.todo_management.controllers import api_todo
from app.business.todo_management.controllers import todo_views

todo_management_router = APIRouter()
todo_management_router.include_router(api_todo.router, tags=["Todo API"])
todo_management_router.include_router(todo_views.router, tags=["Todo Views"])