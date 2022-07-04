from fastapi import APIRouter

from app.business.employee_management.controllers import user

# Include all routers here
api_router = APIRouter()
api_router.include_router(user.router, tags=["users"])
