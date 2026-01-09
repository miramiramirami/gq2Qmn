import aiohttp
from schemas.api import AuthToken, UserResponse

class ReqResApi:
    BASE_URL = "https://reqres.in/api"


    def __init__(self, email, password, session: aiohttp.ClientSession):
        self.email = email
        self.password = password
        self.token: str | None = None
        self._session = session


    async def auth(self):
        payload = {
            "email": self.email,
            "password": self.password
        }

        async with self._session.post(f"{self.BASE_URL}/login", json=payload) as res:
            if res.status != 200:
                text = await res.text()
                raise Exception(f'Ошибка авториазции: {res.status} - {text}')
            data = await res.json()

            print('дата - ', data)

            self.token = AuthToken(**data).token

    
    async def get_users(self) -> list[UserResponse]:

        headers = {"Authorization": f"Bearer {self.token}"}

        async with self._session.get(f'{self.BASE_URL}/users', headers=headers) as res:
            if res.status != 200:
                text = await res.text()
                raise Exception(f'Ошибка получения пользователей: {res.status} - {text}')
            
            data = await res.json()

            return [UserResponse(**item) for item in data["data"]]
