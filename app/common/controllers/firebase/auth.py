import logging
from firebase_admin import auth
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.common import get_user
from app.common.core.identity_provider import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")


class EmailPassword(BaseModel):
    email: str
    password: str


#################################
# Basic Authentication Router
#################################

@router.get("/set-admin")  # Sets current user as admin
def set_user_admin(user: User = Depends(get_user())):
    auth.set_custom_user_claims(user.uid, {"roles": ["admin"]})


@router.get("/login", description="Test Login endpoint that returns a Bearer token authenticating on Firebase "
                                  "Authentication service")
def login(user: EmailPassword = Depends()):
    import requests
    res = requests.post(
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key"
        "=AIzaSyD3T5gpP1hu9FeV9E4g9ZNglqlov-iee9g",
        json={"email": user.email, "password": user.password, "returnSecureToken": "true"})
    return res.json()
