import aiohttp

from osu.abc import User
from .errors import *
from .types.user import PartialUser
from typing import List, Union

class HTTPClient:
    def __init__(self, *, client_id: int, client_secret: str):
        self.id = client_id
        self.secret = client_secret
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.API_URL = "https://osu.ppy.sh/api/v2"
        self.TOKEN_URL = "https://osu.ppy.sh/oauth/token"

    async def _request(self, method: str, url: str, **kwargs):
        resp = await self._session.request(method, url,**kwargs)
        return resp

    async def _get_token(self):
        data = {
            "client_id": self.id,
            "client_secret": self.secret,
            'grant_type':'client_credentials',
            'scope':"public",
        }
        returned = await self._request("POST", self.TOKEN_URL, data=data)
        if returned.status >= 400 <= 403:
            raise HTTPException("401 Unauthorized. Make sure your client_secret is right")
        return (await returned.json())['access_token']

    async def close(self):
        if not self._session.closed:
            await self._session.close()

    async def _make_headers(self):
        authorization = await self._get_token()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {authorization}"
        }

        return headers

    async def get_user(self, user: Union[str, int]) -> PartialUser:
        headers = await self._make_headers()
        return await (await self._request("GET", self.API_URL + f"/users/{user}", headers=headers)).json()

    async def get_beatmap(self, beatmap: Union[str, int]):
        headers = await self._make_headers()
        return await (await self._request("GET", self.API_URL+f"/beatmaps/{beatmap}", headers=headers)).json()
        
    async def get_user_beatmaps(self, /, user: int, type: str, params: dict):
        headers = await self._make_headers()
        return await (await self._request("GET", self.API_URL + f"/users/{user}/beatmapsets/{type}",headers=headers,params=params)).json()

    async def get_user_scores(self, /, user: int, type: str, params: dict):
        headers = await self._make_headers()
        return await (await self._request("GET", self.API_URL + f"/users/{user}/scores/{type}",headers=headers,params=params)).json()
