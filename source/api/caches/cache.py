import redis.asyncio as redis

# redis_client = redis.StrictRedis(host='test_redis', port=6379)
redis_client = redis.StrictRedis(host='localhost', port=6379)


async def clear_cache(key_list: str, key_item: str | None = None, keys_sublist: list[str] | None = None, keys_subitem: list[str] | None = None) -> None:
    await redis_client.delete(key_list)
    if key_item:
        await redis_client.delete(key_item)

    if keys_sublist:
        for key in keys_sublist:
            await redis_client.delete(key)

    if keys_subitem:
        for key in keys_subitem:
            await redis_client.delete(key)


async def get_cache_data(key: str) -> bytes | None:
    cached_data = await redis_client.get(key)
    return cached_data


async def create_cache_data(key: str, object: str) -> None:
    await redis_client.set(key, object)
