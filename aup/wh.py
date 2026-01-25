import aiohttp
import asyncio
import json
from pydantic import BaseModel

class MicrosoftGraphToken(BaseModel):
    access_token: str

class MicrosoftUser(BaseModel):
    userPrincipalName: str

class MicrosoftAPI:
    def __init__(self, tenat_id, client_id, client_secret):
        self.tenat_id = tenat_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f'https://login.microsoftonline.com/{tenat_id}/oauth2/v2.0/token'
        self.scope = "https://graph.microsoft.com/.default"

        self.auth_token = None #токен авторизации

    async def auth(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "grant_type": "client_credentials",
                "tenat_id": self.tenat_id,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.scope
            }
            async with session.post(self.token_url, data=data) as res:
                if res.status == 200:
                    res_json = await res.json()
                    self.auth_token = MicrosoftGraphToken(**res_json).access_token + '1'
                    return True
                raise Exception('Microsoft auth exception')
            
    async def get_users(self,) -> list:
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        current_list = []
        async with aiohttp.ClientSession(headers=headers) as session:
            params={'$top': 10}
            async with session.get('https://graph.microsoft.com/v1.0/users', params=params) as res:
                if res.status == 200:
                    res_json = await res.json()
                    for i in res_json['value']:
                        microsoft_users = MicrosoftUser(**i)
                        current_list.append(microsoft_users)
                    return current_list
                elif res.status == 401:
                    await self.auth() #Пытаемся обновить токен(если будет ошибка авторизации выпадет raise)
                    await self.get_users()
                raise Exception('Error user requests')