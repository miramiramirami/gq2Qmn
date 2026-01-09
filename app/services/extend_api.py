import httpx
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str


class ApiService:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_user(self, user_id: int) -> UserResponse:
        try:
            response = await self._client.get(f"/users/{user_id}")
            response.raise_for_status()
            data = response.json()
            return UserResponse(**data)

        except httpx.HTTPStatusError as e:
            raise ValueError(f"Ошибка запроса к внешнему API: {e}") from e

        except httpx.RequestError as e:
            raise ValueError(f"Ошибка соединения с внешним API: {e}") from e
