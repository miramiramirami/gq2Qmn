from pydantic import BaseModel

class AuthToken(BaseModel):
    token: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str