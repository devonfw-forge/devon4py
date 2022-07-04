import logging
import uvicorn

# Init APP with Configuration
from app import api
from app.common.core.configuration import get_global_settings, get_log_config, get_db_settings
from app.common.core.database import init_db_entities

# Init Logger for this Class
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    init_db_entities(get_db_settings())
    uvicorn.run(api, host="0.0.0.0", port=get_global_settings().port, log_config=get_log_config())
