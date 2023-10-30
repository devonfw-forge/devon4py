import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/todo")

logger = logging.getLogger(__name__)


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse('todo/index.html', {"request": request})
