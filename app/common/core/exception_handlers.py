import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse

from app.common.exceptions.http import DevonHttpException, HTTPError
from app.common.exceptions.runtime import DevonCustomException, ResourceNotFoundException

logger = logging.getLogger(__name__)


def init_exception_handlers(api: FastAPI):
    # Custom HTTP Exception Handler
    @api.exception_handler(DevonHttpException)
    async def http_exception_handler(request: Request, exc):
        logger.error(str(request.url) + " - Path params: " + str(request.path_params) +
                     " - Query Params: " + str(request.query_params))
        # logger.exception(exc.detail)
        logger.error(exc.detail)
        return JSONResponse(content=HTTPError(detail=str(exc.detail)).dict(), status_code=exc.status_code)

    # Custom Runtime Exception Handler
    @api.exception_handler(DevonCustomException)
    async def runtime_exception_handler(request: Request, exc: DevonCustomException):
        logger.error(str(request.url) + " - Path params: " + str(request.path_params) +
                     " - Query Params: " + str(request.query_params))
        logger.exception(exc.detail)
        return PlainTextResponse(str(exc.detail), status_code=500)

    @api.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
        logger.error("Tried to access a resource not available")
        logger.exception(exc.detail)
        return JSONResponse(content=HTTPError(detail=f"Tried to access a resource not available ({exc.detail})").dict(),
                            status_code=404)
