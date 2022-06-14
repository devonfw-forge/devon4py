import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.future import Engine
from sqlmodel import SQLModel

from core.database import get_db_engine, init_db_entities
from core.configuration import GlobalSettings, get_global_settings, get_app, get_log_config, DatabaseSettings, \
    get_db_settings
import logging

# Init APP with Configuration
app = get_app()
# Init Logger for this Class
logger = logging.getLogger(__name__)


@app.get("/info")
def info(settings: GlobalSettings = Depends(get_global_settings)):
    logger.info("TEST INFO")
    logger.error("TEST ERROR")
    logger.debug("TEST DEBUG")
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
    uvicorn.run(app, host="0.0.0.0", port=global_settings.port, log_config=logging_settings)

