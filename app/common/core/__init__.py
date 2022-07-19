from typing import List
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.common.core.configuration import get_global_settings, GlobalSettings
from app.common.core.exception_handlers import init_exception_handlers


def configure_cors(app_settings: GlobalSettings, api: FastAPI):
    # Set CORS enabled origins
    if app_settings.cors and len(app_settings.cors) > 0:
        api.add_middleware(
            CORSMiddleware,
            allow_origins=app_settings.cors,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"]
        )


def get_api(routers: List[APIRouter]):
    app_settings = get_global_settings()
    api = FastAPI(docs_url=app_settings.swagger_path, title=app_settings.app_name)
    # Include selected routers
    for r in routers:
        api.include_router(r)
    # Init exception Handlers
    init_exception_handlers(api)
    # Configure CORS
    configure_cors(app_settings, api)
    # Init infra
    from app.common.infra import configure_api
    configure_api(api)
    return api
