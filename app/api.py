from app.business.router import all_router
from app.common.core import get_api

api = get_api(routers=[all_router])
