from pydantic import BaseSettings
import os
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "My Awesome API"
    environment: str = "TEST"
    swagger_path: str = "docs"

    class Config:
        env_file = "TEST.env"


@lru_cache()
def get_settings():
    # Import + Cache settings (with lru_cache)
    env = os.environ.get("ENV")
    if env:
        return Settings(_env_file="{}.env".format(env))
    else:
        return Settings()
