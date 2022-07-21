from fastapi import APIRouter

from app.common.controllers.firebase import auth

auth_router = APIRouter()
auth_router.include_router(auth.router, tags=["auth"])
