from typing import Optional

from fastapi import Depends

from app.common.exceptions.http import NotFoundException
from app.domain.models import User
from app.domain.repositories.user import get_user_repository, UserRepository


class UserService:
    def __init__(self, repository: UserRepository = Depends(get_user_repository)):
        self.user_repo = repository

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.user_repo.get_by_email(email=email)
        if user is None:
            raise NotFoundException(detail="User not found")
