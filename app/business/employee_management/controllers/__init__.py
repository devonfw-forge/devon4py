from fastapi import APIRouter

from app.business.employee_management.controllers import employee

# Include all routers here
api_router = APIRouter()
api_router.include_router(employee.router, tags=["users"])
