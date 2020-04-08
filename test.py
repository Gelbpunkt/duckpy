import asyncio

from duckpy import Client

client = Client()


async def get_results():
    results = await client.search("tiger")
    print(results[0])
    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(get_results())
