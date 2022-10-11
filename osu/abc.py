from __future__ import annotations
import datetime
from typing import Dict


class User:
    def __init__(self, data):
        self.data = data
        self.username = data.get('username')
        self.global_rank = data.get('statistics').get("global_rank") if data.get('statistics').get("global_rank") is not None else 0
        self.pp = data.get("statistics").get("pp")  if data.get('statistics') else "None"
        self.rank = data.get("statistics").get("grade_counts") if data.get('statistics') else "None"
        self.accuracy = f"{data.get('statistics').get('hit_accuracy'):,.2f}"  if data.get('statistics') else "None"
        self.country_rank = data.get('statistics').get("country_rank") if data.get('statistics').get("country_rank") is not None else 0
        self.profile_order = data['profile_order'] if data['profile_order'] else "Cant Get Profile Order!"
        self.country_emoji = f":flag_{data.get('country_code').lower()}:" if data.get("country_code") else "None"
        self.country_code = data.get("country_code") if data.get("country_code") else "None"
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

        cover_data = self.data['beatmapset']['covers'][cover]
        return cover_data

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
    )

    def __init__(self, data: dict):
        keys = {k: v for k, v in data.items() if k in self.__slots__}
        for k,v in keys.items():
            setattr(self, k, v)
            continue
        
        self.data = data

    def covers(self, cover: str) -> str:
        if cover not in self.data['covers']:
            covers = ', '.join(self.data['covers'])
            return f"Cover not in covers!\nChoose from {covers}"

        cover_data = self.data['covers'][cover]
        return cover_data

class Score:
    def __init__(self, data: dict):
        keys = {k: v for k, v in data.items()}
        for k, v in keys.items():
            setattr(self, k, v)
            continue
        self.beatmapset = Beatmapset(data['beatmapset'])
        self.beatmap = BeatmapCompact(data['beatmap'])