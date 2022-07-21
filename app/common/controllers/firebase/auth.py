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
