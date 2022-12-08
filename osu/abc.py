from __future__ import annotations
import datetime
from typing import Dict, Optional, TYPE_CHECKING

if  TYPE_CHECKING:
    from .types.user import PartialUser


class _BaseUser:
    __slots__ = (
        "username",
        "id",
        "is_bot",
        "avatar_url"
    )
    def __init__(self, data: PartialUser):
        self._update(data)

    def _update(self, data: PartialUser):
        self.username = data['username']
        self.id = data['id']
        self.is_bot = data['is_bot']
        self.avatar_url = data['avatar_url']


class TestUser(_BaseUser):
    def __init__(self, data: PartialUser):
        super().__init__(data)
        self.discord = data['discord']
        self.pp = data['statistics']['pp']
        

class User:
    def __init__(self, data):
        self.data = data
        self.username = data.get('username')
        self.global_rank = data.get('statistics').get("global_rank") if data.get('statistics').get("global_rank") is not None else 0
        self.pp = data.get("statistics").get("pp")  if data.get('statistics') else "None"
        self.rank = data.get("statistics").get("grade_counts") if data.get('statistics') else "None"
        self.accuracy = f"{data.get('statistics').get('hit_accuracy'):,.2f}"  if data.get('statistics') else "None"
        self.country_rank = data.get('statistics').get("country_rank") if data.get('statistics').get("country_rank") is not None else 0
        self.profile_order = data['profile_order'] or "Cant Get Profile Order!"
        self.country_emoji = f":flag_{data.get('country_code').lower()}:" if data.get("country_code") else "None"
        self.country_code = data.get("country_code") or "None"
        self._country = data.get("country")
        self.avatar_url = data.get("avatar_url")
        self.id = data.get("id")
        self.playstyle = data.get("playstyle")
        self.playmode = data.get("playmode")
        self.max_combo = data.get("statistics").get("maximum_combo")
        self.level = data.get("statistics").get("level")
        self.follower_count = data.get("follower_count")
        self.total_hits = data.get("statistics").get("total_hits")
        self.total_score = data.get("statistics").get("total_score")
        self.play_count = data.get("statistics").get("play_count")
        self.replays_watched_count = data['replays_watched_counts']

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} username: {self.username!r}, id: {self.id}>"

    def __str__(self) -> str:
        return self.username


    @property
    def joined_at(self) -> str:
        if self.data.get("join_date"):
           return datetime.datetime.strptime(self.data.get('join_date'), '%Y-%m-%dT%H:%M:%S+00:00')

    @property
    def country(self):
        return [self._country['code'], self._country['name']]

    @property
    def raw(self) -> Dict[str, any]:
        return self.data


class Beatmap:
    def __init__(self, data):
        self.data = data
        self.artist = data['beatmapset']['artist']
        self.title = data['beatmapset']['title']
        self.beatmapset = data['beatmapset']
        self.beatmapset_id = data['beatmapset_id']
        self.difficulty_rating = data['difficulty_rating']
        self.id = data['id']
        self.mode = data['mode']
        self.status = data['status']
        self.difficulty = data['version']
        self.cs = data['cs']
        self.drain = data['drain']
        self.last_updated = datetime.datetime.fromisoformat(data['last_updated'].replace('Z', '')) if data['last_updated'] else None
        self.pass_count = data['passcount']
        self.play_count = data['playcount']
        self.url = data['url']    
        self.favorite_count = data['beatmapset']['favourite_count']
        self.nsfw = data['beatmapset']['nsfw']
        self.ranked_date = datetime.datetime.fromisoformat(data['beatmapset']['ranked_date'].replace('Z', '')) if data['beatmapset']['ranked_date'] else None
        self.submitted_date = datetime.datetime.fromisoformat(data['beatmapset']['submitted_date'].replace('Z', ''))  if data['beatmapset']['submitted_date'] else None
        self.max_combo = data['max_combo']
        self.creator = data['beatmapset']['creator']
        self.ar = data['ar']
        self.bpm = data['bpm']

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title: {self.title!r}, artist: {self.artist!r}>"

    def covers(self, cover: str) -> str:
        if cover not in self.data['beatmapset']['covers']:
            return "Cover not in covers"

        return self.data['beatmapset']['covers'][cover]

class BeatmapCompact:
    __slots__ = (
        "beatmapset_id",
        "difficulty_rating",
        "id",
        "mode",
        "status",
        "total_length",
        "user_id",
        "version"
    )
    def __init__(self, data: dict):
        keys = {k: v for k, v in data.items() if k in self.__slots__}
        for k,v in keys.items():
            setattr(self, k, v)
            continue
        


class Beatmapset:
    __slots__ = (
        "artist",
        "artist_unicode",
        "creator",
        "favourite_count",
        "hype",
        "id",
        "nsfw",
        "offset",
        "play_count",
        "preview_url",
        "source",
        "spotlight",
        "status",
        "title",
        'title_unicode',
        "track_id",
        "user_id",
        "video",
        "json"
    )

    def __init__(self, data: dict):
        self.json = data
        keys = {k: v for k, v in data.items() if k in self.__slots__}
        for k,v in keys.items():
            setattr(self, k, v)
            continue
        
    

    def covers(self, cover: str) -> str:
        if cover not in self.json['covers']:
            covers = ', '.join(self.json['covers'])
            return f"Cover not in covers!\nChoose from {covers}"

        return self.json['covers'][cover]

class Score:
    def __init__(self, data: dict):
        self.accuracy: int = data['accuracy']
        self.best_id: int = data['best_id']
        self.created_at: str = data['created_at']
        self.id: int = data['id']
        self.max_combo: int = data['max_combo']
        self.mode: str = data['mode']
        self.mods: list[str] = data['mods']
        self.passed: bool = data['passed']
        self.perfect: bool = data['perfect']
        self.pp: Optional[int] = data['pp'] or 0 
        self.rank: str = data['rank']
        self.replay: bool = data['replay']
        self.statistics: dict = data['statistics']
        self.user_id: int = data['user_id']
        self.beatmapset = Beatmapset(data['beatmapset'])
        self.beatmap = BeatmapCompact(data['beatmap'])