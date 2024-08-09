import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_menus_is_empty(ac: AsyncClient):
    res = await ac.get('/api/v1/menus/list/0/10')
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_menu(ac: AsyncClient):
    global menu_id
    res = await ac.post('/api/v1/menus/', json={'title': 'My menu 1', 'description': 'My menu description 1'})
    assert res.status_code == 201
    menu_id = res.json()['id']
    resa = await ac.get('/api/v1/menus/list/0/10')
    assert len(resa.json()) == 1


@pytest.mark.asyncio
async def test_update_menu(ac: AsyncClient):
    global menu_id
    res = await ac.patch(f'/api/v1/menus/{menu_id}', json={'title': 'My menu 2', 'description': 'My menu description 2'})
    assert res.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}')
    assert res.json()['title'] == 'My menu 2'
    assert res.json()['description'] == 'My menu description 2'


@pytest.mark.asyncio
async def test_get_all_submenus_is_emplty(ac: AsyncClient):
    global menu_id
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/list/0/10')
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    res = await ac.post(f'/api/v1/menus/{menu_id}/submenus/',
                        json={'title': 'My submenu 1', 'description': 'My submenu description 1'})
    assert res.status_code == 201
    submenu_id = res.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_update_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    res = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={'title': 'My submenu 2', 'description': 'My submenu description 2'})
    assert res.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert res.json()['title'] == 'My submenu 2'
    assert res.json()['description'] == 'My submenu description 2'


@pytest.mark.asyncio
async def test_get_all_dishes_is_empty(ac: AsyncClient):
    global menu_id
    global submenu_id
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/list/0/10')
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    res = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                        json={'title': 'My dish 1', 'description': 'My dish description 1', 'price': 12.50})
    assert res.status_code == 201
    dish_id = res.json()['id']
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/list/0/10')
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_update_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    res = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json={
        'title': 'My updated dish 1', 'description': 'My updated dish description 1', 'price': 14.5})
    assert res.status_code == 200
    res = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert res.json()['title'] == 'My updated dish 1'
    assert res.json()['description'] == 'My updated dish description 1'
    assert res.json()['price'] == '14.5000000000000000000000000000'


@pytest.mark.asyncio
async def test_delete_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    res = await ac.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/list/0/10')
    assert res.json() == []


@pytest.mark.asyncio
async def test_delete_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    res = await ac.get('/api/v1/menus/{menu_id}/submenus/list/0/10')
    assert res.json() == []


@pytest.mark.asyncio
async def test_delete_menu(ac: AsyncClient):
    global menu_id
    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    res = await ac.get('/api/v1/menus/list/0/10')
    assert res.json() == []
