from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_db_session_factory
from app.models import User
from app.models.user import UserCreateRequest
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    async def get_by_email(self, *, email: str) -> Optional[User]:
        async with self.create_session() as db_session:
            users = await db_session.execute(select(User).where(User.email == email))
            result = users.first()
        return result

    async def create_with_role(self, *, req: UserCreateRequest) -> User:
        async with self.create_session() as db_session:
            db_obj = User(
                first_name=req.first_name,
                last_name=req.last_name,
                email=req.email,
                is_superuser=req.is_superuser,
                # hashed_password=get_password_hash(obj_in.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                role_id=req.role_id
            )
            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
            return db_obj


def get_user_repository(session_factory: sessionmaker = Depends(get_db_session_factory)):
    return UserRepository(User, session_factory)
