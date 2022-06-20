import logging

from fastapi import APIRouter, Depends

from app.core.configuration import GlobalSettings, get_global_settings
from app.services.user import UserService

router = APIRouter(prefix="/users")

logger = logging.getLogger(__name__)


@router.get("/info")
async def info(user_service: UserService = Depends(UserService)):
    logger.info("TEST INFO")
    logger.error("TEST ERROR")
    logger.debug("TEST DEBUG")
    await user_service.get_user_by_email(email="test@email.es")
    return {}
