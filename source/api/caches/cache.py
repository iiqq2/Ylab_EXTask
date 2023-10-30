import redis.asyncio as redis


redis_client = redis.StrictRedis(host='ylab_redis', port=6379)
# redis_client = redis.StrictRedis(host='localhost', port=6379)


async def clear_cache() -> None:
    await redis_client.flushall()


async def get_cache_data(url) -> bytes | None:
    cached_data = await redis_client.get(url)
    return cached_data


async def create_cache_data(url, time, object) -> None:
    await redis_client.setex(url, time, object)
