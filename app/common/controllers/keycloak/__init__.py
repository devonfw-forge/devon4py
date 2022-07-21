# Include all routers here
from fastapi import APIRouter

from app.common.controllers.keycloak import identity, auth

auth_router = APIRouter()
auth_router.include_router(auth.router, tags=["auth"])
auth_router.include_router(identity.router, tags=["idp"])
