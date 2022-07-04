from fastapi import APIRouter

# Include all routers here
from app.business.todo_management.controllers import todo_management_router

all_router = APIRouter()
all_router.include_router(todo_management_router, tags=["Todo Management"])
