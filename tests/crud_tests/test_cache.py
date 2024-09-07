import pytest
from httpx import AsyncClient

from source.api.cache.config import MENU_LIST_CACHE_KEY


@pytest.mark.redis
async def test_redis_key_operations(ac: AsyncClient, redis_clients):
    resp = await ac.get('/api/v1/menus/list/0/10')
    print(resp)

    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 1
