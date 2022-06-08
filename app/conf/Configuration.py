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
