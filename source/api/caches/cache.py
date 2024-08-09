import redis.asyncio as redis

# redis_client = redis.StrictRedis(host='test_redis', port=6379)
redis_client = redis.StrictRedis(host='localhost', port=6379)


async def clear_cache(key_list: str, key_item: str | None = None, keys_sublist: list[str] | None = None, keys_subitem: list[str] | None = None) -> None:
    """ Это функция очистки кэша. Благодаря ней мы можем забыть про использование ttl, и наши данные всегда будут актуальными.
    Основная сущность - сущность из которой мы вызываем эту функцию
    Подсущности - сущности, данные которых мы должны удалить, в ходе удаления данных основной сущности, чтобы не потерять согласованность

    Args:
        key_list (str): Ключ get_all эндпоинта основной сущности
        key_item (str | None, optional): Ключ get эндпоинта основной сущности. Defaults to None.
        keys_sublist (list[str] | None, optional): Список с ключами get_all эндпоинтов подсущностей. Defaults to None.
        keys_subitem (list[str] | None, optional): Список с ключами get эндпоинтов подсущностей. Defaults to None.
    """

    keys = []
    async for key in redis_client.scan_iter(f'{key_list}*'):
        keys.append(key)
    if keys:
        await redis_client.unlink(*keys)

    if key_item:
        await redis_client.delete(key_item)

    if keys_sublist:
        keys = []
        for key_list_ in keys_sublist:
            async for key in redis_client.scan_iter(f'{key_list_}*'):
                keys.append(key)
            if keys:
                await redis_client.unlink(*keys)

    if keys_subitem:
        await redis_client.unlink(*keys_subitem)


async def get_cache_data(key: str) -> bytes | None:
    cached_data = await redis_client.get(key)
    return cached_data


async def create_cache_data(key: str, object: str) -> None:
    await redis_client.set(key, object)
