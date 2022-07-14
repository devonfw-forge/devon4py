from typing import Optional

from fastapi import Depends

from app.common.exceptions.http import NotFoundException
from app.domain.models import Employee
from app.domain.repositories.employee import get_employee_repository, EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository = Depends(get_employee_repository)):
        self.user_repo = repository

    async def get_user_by_email(self, email: str) -> Optional[Employee]:
        user = await self.user_repo.get_by_email(email=email)
        if user is None:
            raise NotFoundException(detail="User not found")
