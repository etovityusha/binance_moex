import httpx


async def get_async(url: str, data: dict, key: str) -> None:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
    data[key] = response.json()
