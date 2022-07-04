from fastapi import APIRouter

# Include all routers here
from app.business.todo_management.controllers import todo

todo_management_router = APIRouter()
todo_management_router.include_router(todo.router, tags=["Todo"])
