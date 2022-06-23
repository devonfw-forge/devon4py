from fastapi import APIRouter

from app.controllers import user, auth, identity

# Include all routers here
api_router = APIRouter()
api_router.include_router(user.router, tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(identity.router, tags=["idp"])
