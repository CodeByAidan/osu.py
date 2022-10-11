from __future__ import annotations
import aiohttp
from typing import Union, List
from .errors import *
from .abc import *

class Client:
    def __init__(self, *, client_id: int, client_secret: str):
        self.id = client_id
        self.secret = client_secret
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.API_URL = "https://osu.ppy.sh/api/v2"
        self.TOKEN_URL = "https://osu.ppy.sh/oauth/token"
        self.beatmap_types = ['favourite', 'graveyard', 'loved', 'most_played', 'pending', 'ranked']
        self.special_types = ['most_played']
        self.score_types = ['best', 'firsts', 'recent']

    async def _request(self, method: str, url: str, **kwargs):
        async with self.session.request(method, url,**kwargs) as resp:
            json = await resp.json()

        return json


    async def _get_token(self):
        data = {
            "client_id": self.id,
            "client_secret": self.secret,
            'grant_type':'client_credentials',
            'scope':"public",
        }

        async with self.session.post(self.TOKEN_URL,data=data) as response:
            return (await response.json())['access_token']
    
    async def _make_headers(self):
        authorization = await self._get_token()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {authorization}"
        }

        return headers

    async def fetch_user(self, user: Union[str, int]) -> User:
        """Fetches a user using either an ID or Username"""
        headers = await self._make_headers()

        params = {
            "limit":5
        }
        json = await self._request("GET", url=self.API_URL+f"/users/{user}", headers=headers, params=params)

        if 'error' in json.keys() and json['error'] is None:
            raise NoUserFound("No user was found by that name!")

        return User(json)

    async def fetch_user_score(self, user: Union[str, int], /, type: str, limit: int = 1, include_fails: bool = False):
        """Fetches scores for a user based on a type and limit"""

        if type not in self.score_types:
            types = ', '.join(self.score_types)
            raise ValueError(f"Score type must be in {types}")

        headers = await self._make_headers()

        params = {
            "limit": limit,
            "include_fails": f"{0 if include_fails is not True else 1}"
        }

        json = await self._request("GET", self.API_URL+f"/users/{user}/scores/{type}", headers=headers, params=params)

        beatmaps = []
        
        for beatmap in json:
            beatmaps.append(Score(beatmap))
                
        return beatmaps

    async def fetch_user_beatmaps(self, /, user: int, type: str, limit: int) -> List | Beatmapset:
        """Fetches beatmaps for a user based on a type and limit"""
        headers = await self._make_headers()
        params = {
            "limit": limit
        }
        
        if type not in self.beatmap_types:
            types = ', '.join(self.beatmap_types)
            raise ValueError(f"Beatmap type must be in {types}")

        json = await self._request("GET", self.API_URL + f"/users/{user}/beatmapsets/{type}",headers=headers,params=params)
    
        beatmaps = []
        
        for beatmap in json:
            if type in self.special_types:
                beatmaps.append({"beatmapset":Beatmapset(beatmap['beatmapset']), "beatmap": BeatmapCompact(beatmap['beatmap'])})
            else:
                beatmaps.append(Beatmapset(beatmap))
                
        return beatmaps
    
    async def _tests(self, method: str, /, endpoint: str, params: dict = None):
        headers = await self._make_headers()
        async with self.session.request(method, self.API_URL + endpoint, params=params, headers=headers) as resp:
            json = await resp.json()

        return json

    async def fetch_beatmap(self, beatmap: Union[str, int]): 
        """Fetches a beatmap"""

        headers = await self._make_headers()

        json = await self._request("GET", self.API_URL+f"/beatmaps/{beatmap}", headers=headers)

        if 'error' in json.keys():
            raise NoBeatMapFound("No beatmap was found by that ID!")

        return Beatmap(json)

    async def close(self):
        await self.session.close()