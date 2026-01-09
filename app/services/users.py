from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from sqlalchemy import select
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class UserService:
    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User]:
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession) -> User:
        user = User(email=data.email, password=data.password)

        try:
            async with session.begin():
                session.add(user)
            await session.refresh(user)
            return user
        except IntegrityError as e:
            raise ValueError(f"Ошибка создания пользователя - {e.orig}") from e

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
        try:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка получения пользователя: {e}") from e
