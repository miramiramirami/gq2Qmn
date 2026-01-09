from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.get_session import get_session
from services.users import UserService
from schemas.users import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    return await UserService.get_all_users(session)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    return await UserService.create_user(data, session)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    return await UserService.get_user_by_id(user_id, session)
