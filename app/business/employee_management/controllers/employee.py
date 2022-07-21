import logging

from fastapi import APIRouter, Depends

from app.business.employee_management.services.employee import EmployeeService

router = APIRouter(prefix="/users")

logger = logging.getLogger(__name__)


@router.get("/info")
async def info(employee_service: EmployeeService = Depends(EmployeeService)):
    logger.info("TEST INFO")
    logger.error("TEST ERROR")
    logger.debug("TEST DEBUG")
    await employee_service.get_user_by_email(email="test@email.es")
    return {}
