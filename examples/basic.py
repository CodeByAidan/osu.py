import osu
import asyncio

async def main():
    async with osu.Client(client_id=yourclientid, client_secret="YourClientSecret") as client: # Async with because it auto closes session.
        user = await client.fetch_user("Sawsha") #Returns a User object

        return user.username

asyncio.set_event_loop().run_until_complete(main())