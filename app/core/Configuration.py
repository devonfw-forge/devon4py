import yaml
from fastapi import FastAPI
from pydantic import BaseSettings
import os
from functools import lru_cache


class GlobalSettings(BaseSettings):
    app_name: str = "My Awesome API"
    environment: str = "TEST"
    port: int = 80
    swagger_path: str = "docs"

    class Config:
        env_file = "TEST.env"


@lru_cache()
def get_global_settings():
    # Import + Cache settings (with lru_cache)
    env = os.environ.get("ENV")
    if env:
        return GlobalSettings(_env_file="{}.env".format(env))
    else:
        return GlobalSettings()


@lru_cache()
def get_log_config():
    with open("logging.yaml") as logconf:
        log_config = yaml.safe_load(logconf)
        return log_config


def get_app():
    app_settings = get_global_settings()
    app = FastAPI(docs_url=app_settings.swagger_path)
    return app
