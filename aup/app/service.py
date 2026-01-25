import aiohttp
from app.exceptions import GetInfoError, GetTokenError
from pydantic import BaseModel

class BearerToken(BaseModel):
    token: str


class ApiReq:
    def __init__(self, *, token, email, password, session: aiohttp.ClientSession):
        self.token = token
        self.email = email
        self.password = password
        self._session = session

    async def get_info(self):
        async with self._session.get('https://httpbin.org/get') as res:
            if res.status != 200:
                text = await res.text()
                raise GetInfoError(f"HTTP {res.status}: {text}")
            return await res.json()


    async def auth(self):
        header = {"Authorization ": f"Bearer {self.token}"}

        async with self._session.get('https://httpbin.org/bearer', headers=header) as res:
            if res.status != 200:
                text = await res.text()
                raise GetTokenError(f"HTTP {res.status}: {text}")
            data = await res.json()

            return BearerToken(**data).token
        