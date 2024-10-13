from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from source.api.cache.cache import clear_cache
from source.api.cache.config import (
    DISH_ITEM_CACHE_KEY,
    DISH_LIST_CACHE_KEY,
    MENU_ITEM_CACHE_KEY,
    MENU_LIST_CACHE_KEY,
    SUBMENU_ITEM_CACHE_KEY,
    SUBMENU_LIST_CACHE_KEY,
)
from source.api.cache.decorators import cache_item_response, cache_list_response
from source.api.factories.factory import RepositoryFactory
from source.api.repositories.interfaces import BaseService
from source.api.schems.schemas import DishScheme, MenuScheme, SubmenuScheme


class MenuService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    # @cache_list_response(cache_key_prefix=MENU_LIST_CACHE_KEY)
    async def get_all(self, skip: int, limit: int) -> JSONResponse:
        repository = await RepositoryFactory.create('menu', self.db)
        menus_list = await repository.get_all(skip=skip, limit=limit)
        return JSONResponse(content=menus_list, status_code=status.HTTP_200_OK)

    # @cache_item_response(cache_key_prefix=MENU_ITEM_CACHE_KEY)
    async def get(self, menu_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('menu', self.db)
        menu = await repository.get(menu_id)
        if menu is not None:
            return JSONResponse(content=menu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'menu not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, menu_schema: MenuScheme) -> JSONResponse:
        await clear_cache(MENU_LIST_CACHE_KEY)
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.create(title=menu_schema.title, description=menu_schema.description)

        return JSONResponse(content=menu_data, status_code=status.HTTP_201_CREATED)

    async def update(self, menu_id: UUID, menu_schema: MenuScheme) -> JSONResponse:
        await clear_cache(key_list=MENU_LIST_CACHE_KEY, key_item=f'{MENU_ITEM_CACHE_KEY}_{menu_id}')
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.update(id=menu_id, title=menu_schema.title, description=menu_schema.description)

        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)

    async def delete(self, menu_id: UUID) -> JSONResponse:
        await clear_cache(key_list=MENU_LIST_CACHE_KEY, key_item=f'{MENU_ITEM_CACHE_KEY}_{menu_id}')
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.delete(id=menu_id)

        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)


class SubMenuService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    # @cache_list_response(cache_key_prefix=SUBMENU_LIST_CACHE_KEY)
    async def get_all(self, skip: int, limit: int) -> JSONResponse:
        repository = await RepositoryFactory.create('submenu', self.db)
        submenus_list = await repository.get_all(skip=skip, limit=limit)
        return JSONResponse(content=submenus_list, status_code=status.HTTP_200_OK)

    # @cache_item_response(cache_key_prefix=SUBMENU_ITEM_CACHE_KEY)
    async def get(self, submenu_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu = await repository.get(id=submenu_id)
        if submenu is not None:
            return JSONResponse(content=submenu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, menu_id: UUID, submenu_schema: SubmenuScheme) -> JSONResponse:
        await clear_cache(key_list=SUBMENU_LIST_CACHE_KEY, keys_sublist=[MENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}'])
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.create(menu_id=menu_id, title=submenu_schema.title,
                                               description=submenu_schema.description)

        return JSONResponse(content=submenu_data, status_code=status.HTTP_201_CREATED)

    async def update(self, menu_id: UUID, submenu_id: UUID, submenu_schema: SubmenuScheme) -> JSONResponse:
        await clear_cache(key_list=SUBMENU_LIST_CACHE_KEY, key_item=f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}', keys_sublist=[MENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}'])
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.update(id=submenu_id, title=submenu_schema.title,
                                               description=submenu_schema.description)

        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        await clear_cache(key_list=SUBMENU_LIST_CACHE_KEY, key_item=f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}', keys_sublist=[MENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}'])
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.delete(submenu_id)

        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)


class DishService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    # @cache_list_response(cache_key_prefix=DISH_LIST_CACHE_KEY)
    async def get_all(self, skip: int, limit: int) -> JSONResponse:
        repository = await RepositoryFactory.create('dish', self.db)
        dishes_list = await repository.get_all(skip=skip, limit=limit)
        return JSONResponse(content=dishes_list, status_code=status.HTTP_200_OK)

    # @cache_item_response(cache_key_prefix=DISH_ITEM_CACHE_KEY)
    async def get(self, dish_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('dish', self.db)
        dish = await repository.get(dish_id=dish_id)
        if dish is not None:
            return JSONResponse(content=dish, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'dish not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, dish_schema: DishScheme, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        await clear_cache(key_list=DISH_LIST_CACHE_KEY, keys_sublist=[MENU_LIST_CACHE_KEY, SUBMENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}', f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}'])
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.create(submenu_id=submenu_id, title=dish_schema.title,
                                            price=dish_schema.price, description=dish_schema.description)

        return JSONResponse(content=dish_data, status_code=status.HTTP_201_CREATED)

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish_schema: DishScheme) -> JSONResponse:
        await clear_cache(key_list=DISH_LIST_CACHE_KEY, key_item=f'{DISH_ITEM_CACHE_KEY}_{dish_id}', keys_sublist=[MENU_LIST_CACHE_KEY, SUBMENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}', f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}'])
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.update(title=dish_schema.title, price=dish_schema.price,
                                            description=dish_schema.description, id=dish_id)

        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        await clear_cache(key_list=DISH_LIST_CACHE_KEY, key_item=f'{DISH_ITEM_CACHE_KEY}_{dish_id}', keys_sublist=[MENU_LIST_CACHE_KEY, SUBMENU_LIST_CACHE_KEY], keys_subitem=[f'{MENU_ITEM_CACHE_KEY}_{menu_id}', f'{SUBMENU_ITEM_CACHE_KEY}_{submenu_id}'])
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.delete(dish_id)

        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)
