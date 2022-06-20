import logging
import uvicorn
from fastapi import Depends

from app.core.configuration import get_global_settings, get_api, get_log_config, get_db_settings, GlobalSettings
from app.core.database import init_db_entities

# Init APP with Configuration
from app.services.user import UserService

api = get_api()
# Init Logger for this Class
logger = logging.getLogger(__name__)


@api.get("/info")
async def info(settings: GlobalSettings = Depends(get_global_settings),
               user_service: UserService = Depends(UserService)):
    logger.info("TEST INFO")
    logger.error("TEST ERROR")
    logger.debug("TEST DEBUG")
    await user_service.get_user_by_email(email="test@email.es")
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "swagger": settings.swagger_path if settings.swagger_path else "DISABLED"
    }

if __name__ == "__main__":
    global_settings = get_global_settings()
    logging_settings = get_log_config()
    db_settings = get_db_settings()
    init_db_entities(db_settings)
    print(global_settings.port, global_settings.environment)
    uvicorn.run(api, host="0.0.0.0", port=global_settings.port, log_config=logging_settings)
