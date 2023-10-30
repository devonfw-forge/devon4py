from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

# Include all routers here
from app.business.todo_management.router import todo_management_router

all_router = APIRouter()
all_router.include_router(todo_management_router, tags=["Todo Management"])


@all_router.get("/")
async def home_page_redirect(request: Request):
    return RedirectResponse("/todos")
