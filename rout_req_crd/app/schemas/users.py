from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

    model_config = {'extra': 'forbid'}

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int