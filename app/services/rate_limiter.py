from fastapi import HTTPException
from app.core.redis import redis_client


RATE_LIMIT = 10
WINDOW = 60


def check_rate_limit(user_id: int):

    key = f"rate_limit:user:{user_id}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > RATE_LIMIT:

        raise HTTPException(status_code=429, detail="Rate limit exceeded")
