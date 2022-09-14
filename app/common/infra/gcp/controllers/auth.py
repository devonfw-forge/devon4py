import logging
from firebase_admin import auth
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.common import get_user
from app.common.core.identity_provider import User
from app.common.infra.gcp.firebase import get_account_info, get_firebase_settings, FirebaseSettings

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
def login(user: EmailPassword = Depends(), firebase_config: FirebaseSettings = Depends(get_firebase_settings)):
    import requests
    api_key = firebase_config.api_key
    res = requests.post(
        f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}",
        json={"email": user.email, "password": user.password, "returnSecureToken": "true"})
    return res.json()
