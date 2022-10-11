import logging

logger = logging.getLogger(__name__)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
from osu import Client
import asyncio

async def main():
    async with Client(client_id=15748, client_secret="V9lAyJIUVJiyUTFr5iDHfrwV5qOmbXV6shnZe3Ot") as client:
        user = await client.fetch_user("Sawsha")

    print(user)

asyncio.run(main())