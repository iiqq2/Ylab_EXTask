import redis


# redis_client = redis.StrictRedis(host='ylab_redis', port=6379)
redis_client = redis.StrictRedis(host='localhost', port=6379)


def clear_cache() -> None:
    redis_client.flushall()


def get_cache_data(url) -> bytes | None:
    cache_data = redis_client.get(url)
    return cache_data


def create_cache_data(url, time, object) -> None:
    redis_client.setex(url, time, object)