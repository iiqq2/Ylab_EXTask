import pytest
from httpx import AsyncClient

from source.api.cache.config import (
    DISH_ITEM_CACHE_KEY,
    DISH_LIST_CACHE_KEY,
    MENU_ITEM_CACHE_KEY,
    MENU_LIST_CACHE_KEY,
    SUBMENU_ITEM_CACHE_KEY,
    SUBMENU_LIST_CACHE_KEY,
)


# Menu
@pytest.mark.redis
@pytest.mark.asyncio
async def test_menu_cache_on_get_list(ac: AsyncClient, redis_clients):
    await ac.get('/api/v1/menus/list/0/10')
    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 1


@pytest.mark.redis
@pytest.mark.asyncio
async def test_menu_cache_on_create(ac: AsyncClient, redis_clients):
    global menu_id
    res = await ac.post('/api/v1/menus/', json={'title': 'New Menu', 'description': 'New Description'})
    menu_id = res.json()['id']
    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0


@pytest.mark.redis
@pytest.mark.asyncio
async def test_menu_cache_on_get_item(ac: AsyncClient, redis_clients):
    global menu_id
    await ac.get(f'/api/v1/menus/{menu_id}')
    assert await redis_clients.exists(f'{MENU_ITEM_CACHE_KEY}_{menu_id}') == 1


@pytest.mark.redis
@pytest.mark.asyncio
async def test_menu_cache_on_delete(ac: AsyncClient, redis_clients):
    global menu_id
    await ac.delete(f'/api/v1/menus/{menu_id}')
    assert await redis_clients.exists(f'{MENU_ITEM_CACHE_KEY}_{menu_id}') == 0


@pytest.mark.redis
@pytest.mark.asyncio
async def test_menu_cache_on_create2(ac: AsyncClient, redis_clients):
    global menu_id
    res = await ac.post('/api/v1/menus/', json={'title': 'New Menu', 'description': 'New Description'})
    menu_id = res.json()['id']
    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0

# Submenu


@pytest.mark.redis
@pytest.mark.asyncio
async def test_submenu_cache_on_get_list(ac: AsyncClient, redis_clients):
    global menu_id
    await ac.get(f'/api/v1/menus/{menu_id}/submenus/list/0/10')
    assert await redis_clients.exists(f'{SUBMENU_LIST_CACHE_KEY}_skip:0_limit:10') == 1


@pytest.mark.redis
@pytest.mark.asyncio
async def test_submenu_cache_on_create(ac: AsyncClient, redis_clients):
    global submenu_id
    res = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={'title': 'New Submenu', 'description': 'Submenu Description'})
    submenu_id = res.json()['id']
    assert await redis_clients.exists(f'{SUBMENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0
    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0


@pytest.mark.redis
@pytest.mark.asyncio
async def test_submenu_cache_on_get_item(ac: AsyncClient, redis_clients):
    global submenu_id
    global menu_id
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    print(222222222, res.json())
    assert await redis_clients.exists(f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}') == 1


@pytest.mark.redis
@pytest.mark.asyncio
async def test_submenu_cache_on_delete(ac: AsyncClient, redis_clients):
    global submenu_id
    await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert await redis_clients.exists(f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}') == 0


@pytest.mark.redis
@pytest.mark.asyncio
async def test_submenu_cache_on_create2(ac: AsyncClient, redis_clients):
    global submenu_id
    res = await ac.post(f'/api/v1/menus/{menu_id}/submenus/', json={'title': 'New Submenu', 'description': 'Submenu Description'})
    submenu_id = res.json()['id']
    assert await redis_clients.exists(f'{SUBMENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0
    assert await redis_clients.exists(f'{MENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0

# Dish
# @pytest.mark.redis
# @pytest.mark.asyncio
# async def test_dish_cache_on_get_list(ac: AsyncClient, redis_clients):
#     global submenu_id
#     await ac.get(f'/api/v1/submenus/{submenu_id}/dishes/list/0/10')
#     assert await redis_clients.exists(f'{DISH_LIST_CACHE_KEY}_skip:0_limit:10') == 1

# @pytest.mark.redis
# @pytest.mark.asyncio
# async def test_dish_cache_on_create(ac: AsyncClient, redis_clients):
#     global dish_id
#     res = await ac.post(f'/api/v1/submenus/{submenu_id}/dishes/', json={"title": "New Dish", "price": 10.99, "description": "Dish Description"})
#     dish_id = res.json()['id']
#     assert await redis_clients.exists(f'{DISH_LIST_CACHE_KEY}_skip:0_limit:10') == 0
#     assert await redis_clients.exists(f'{SUBMENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0

# @pytest.mark.redis
# @pytest.mark.asyncio
# async def test_dish_cache_on_get_item(ac: AsyncClient, redis_clients):
#     global dish_id
#     await ac.get(f'/api/v1/submenus/{submenu_id}/dishes/{dish_id}')
#     assert await redis_clients.exists(f'{DISH_ITEM_CACHE_KEY}_{dish_id}') == 1

# @pytest.mark.redis
# @pytest.mark.asyncio
# async def test_dish_cache_on_delete(ac: AsyncClient, redis_clients):
#     global dish_id
#     await ac.delete(f'/api/v1/submenus/{submenu_id}/dishes/{dish_id}')
#     assert await redis_clients.exists(f'{DISH_ITEM_CACHE_KEY}_{dish_id}') == 0

# @pytest.mark.redis
# @pytest.mark.asyncio
# async def test_dish_cache_on_create2(ac: AsyncClient, redis_clients):
#     global submenu_id
#     res = await ac.post(f'/api/v1/submenus/{submenu_id}/dishes', json={"title": "New Dish", "price": 10.99, "description": "Dish Description"})
#     dish_id = res.json()['id']
#     assert await redis_clients.exists(f'{DISH_LIST_CACHE_KEY}_skip:0_limit:10') == 0
#     assert await redis_clients.exists(f'{SUBMENU_LIST_CACHE_KEY}_skip:0_limit:10') == 0
