import aiohttp
from pydantic import BaseModel, Field

class Token(BaseModel):
    token: str

class Headers(BaseModel):
    accept: str = Field(alias="Accept")
    accept_encoding: str = Field(alias="Accept-Encoding")
    host: str = Field(alias="Host")
    user_agent: str = Field(alias="User-Agent")

    model_config = {
        "populate_by_name": True
    }

class TestApi:
    def __init__(self, token, user, password, session: aiohttp.ClientSession):
        self.token = token
        self.user = user
        self.password = password
        self._session = session


    async def get_bin(self):
        async with self._session.get("https://httpbin.org/get") as res:
            if res.status != 200:
                text = await res.text()
                raise Exception(f'Ошибка запроса -  {text}')
            data = await res.json()

            return Headers(**data['headers'])
        

    async def auth(self):
        async with self._session.get(
            f"https://httpbin.org/basic-auth/{self.user}/{self.password}",
            auth=aiohttp.BasicAuth(self.user, self.password)
        ) as res:
            if res.status != 200:
                text = await res.text()
                raise Exception(f"Ошибка авторизации: {res.status}, {text}")
            
            data = await res.json()
            return data
        

    async def bearer_auth(self):
        headers = {"Authorization": f"Bearer {self.token}"}

        async with self._session.get("https://httpbin.org/bearer", headers=headers) as res:
            if res.status != 200:
                text = await res.text()
                raise Exception(f"Ошибка авторизации: {res.status}, {text}")
            
            data = await res.json()
            return Token(**data).token