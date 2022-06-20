from typing import Optional

from fastapi import Depends

from app.models import User
from app.repositories.user import get_user_repository, UserRepository


class UserService:
    def __init__(self, repository: UserRepository = Depends(get_user_repository)):
        self.user_repo = repository

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_by_email(email=email)
