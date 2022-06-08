from fastapi import Depends, FastAPI
from conf.Configuration import Settings, get_settings

app = FastAPI(docs_url=get_settings().swagger_path)


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "swagger": settings.swagger_path if settings.swagger_path else "DISABLED"
    }
