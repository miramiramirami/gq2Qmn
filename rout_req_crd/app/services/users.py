from app.schemas.users import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.schemas.exceptions import UserAlreadyExistsError

class UserService:
    @staticmethod
    async def create_user(*, name: str, email: str, session: AsyncSession) -> User:
        exists = await session.scalar(select(User).where(User.email == email))

        if exists:
            raise UserAlreadyExistsError()


        user = User(
            name = name,
            email = email
        )

        session.add(user)

        try: 
            await session.flush()
        except IntegrityError:
            await session.rollback()
            raise UserAlreadyExistsError()
            
        
        await session.refresh(user)
        return user
            

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User]:
        res = await session.execute(select(User))
        return res.scalars().all()