import asyncio
import osu

async def main():
    client = osu.Client(client_secret="V9lAyJIUVJiyUTFr5iDHfrwV5qOmbXV6shnZe3Ot", client_id=15748)
    print((await client.fetch_user("Sawsha")).username)
    await client.close()

asyncio.run(main())