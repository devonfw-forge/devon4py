from fastapi import APIRouter

from app.controllers import user

api_router = APIRouter()
api_router.include_router(user.router, tags=["users"])
