from __future__ import annotations

import os
from functools import lru_cache
from typing import Type, List, TypeVar

import yaml
from pydantic import BaseSettings, AnyHttpUrl, validator

SettingsType = TypeVar('SettingsType', bound=BaseSettings)


# Configuration Objects Definitions
class GlobalSettings(BaseSettings):
    app_name: str = "My Awesome API"
    environment: str = "TEST"
    port: int = 80
    swagger_path: str = "/docs"
    cors: List[str] | List[AnyHttpUrl] = []

    @validator("cors", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if v is None:
            print("CORS Not Specified")
            return []
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = "TEST.env"


# Utils to load Configurations

def load_env_file_on_settings(settings: Type[SettingsType]) -> SettingsType:
    env = os.environ.get("ENV")
    if env:
        return settings(_env_file="{}.env".format(env))
    else:
        return settings()


@lru_cache()
def get_global_settings() -> GlobalSettings:
    return load_env_file_on_settings(GlobalSettings)


@lru_cache()
def get_log_config():
    with open("logging.yaml") as logconf:
        log_config = yaml.safe_load(logconf)
        return log_config
