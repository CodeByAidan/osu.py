from typing import TypedDict, Optional

class PartialUser(TypedDict):
    id: int
    username: str
    avatar_url: str