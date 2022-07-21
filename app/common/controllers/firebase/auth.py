import logging
from firebase_admin import auth
from fastapi import APIRouter, Depends
from app.common import get_user, idp
from app.common.core.identity_provider import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")


#################################
# Basic Authentication Router
#################################

@router.get("/set-admin")  # Sets current user as admin
def set_user_admin(user: User = Depends(get_user())):
    auth.set_custom_user_claims(user.uid, {"roles": ["admin"]})
