from fastapi import APIRouter, Depends, HTTPException
from db.database import get_session
from app.schemas.users import UserResponse, UserCreate
from app.schemas.exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import UserService

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await UserService.get_all_users(session)


@router.post('/', response_model=UserResponse)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await UserService.create_user(
            name=data.name,
            email=data.email,
            session=session
        )
    
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )