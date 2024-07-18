import redis.asyncio as redis

# redis_client = redis.StrictRedis(host='test_redis', port=6379)
redis_client = redis.StrictRedis(host='localhost', port=6379)


async def clear_cache() -> None:
    await redis_client.flushall()


async def get_cache_data(key: str) -> bytes | None:
    cached_data = await redis_client.get(key)
    return cached_data


async def create_cache_data(key: str, time: int, object: str) -> None:
    await redis_client.setex(key, time, object)
