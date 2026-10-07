import httpx
import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:9000"
)


async def forward_request(method: str, path: str):
    url = f"{BACKEND_URL}{path}"

    async with httpx.AsyncClient() as client:

        response = await client.request(method=method, url=url)

    return response
