from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import select, Session

from app.common.base.base_repository import BaseRepository
from app.common.core.database import get_session
from app.common.exceptions.http import NotFoundException
from app.domain.models.employee import Employee


class EmployeeRepository(BaseRepository[Employee]):

    def get_by_email(self, *, email: str) -> Optional[Employee]:
        employees = self.session.exec(select(Employee).where(Employee.mail == email))
        employee = employees.one_or_none()
        if not employee:
            raise NotFoundException(detail="Employee with email {} not found".format(email))
        return employee

    def create(self, *, email: str, name: Optional[str] = None, surname: Optional[str]) -> Employee:
        new_employee = Employee(email=email, name=name, surname=surname)
        self.session.add(new_employee)
        self.session.commit()
        self.session.refresh(new_employee)
        return new_employee


def get_employee_repository(session: Session = Depends(get_session)):
    return EmployeeRepository(Employee, session)
