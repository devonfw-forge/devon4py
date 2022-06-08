import uvicorn
from fastapi import Depends, FastAPI
from conf.Configuration import GlobalSettings, get_global_settings

app_settings = get_global_settings()
app = FastAPI(docs_url=app_settings.swagger_path)


@app.get("/info")
async def info(settings: GlobalSettings = Depends(get_global_settings)):
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "swagger": settings.swagger_path if settings.swagger_path else "DISABLED"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=app_settings.port)
