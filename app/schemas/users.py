from pydantic import EmailStr, BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(extra="forbid")


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] | None
    password: Optional[str] | None


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
