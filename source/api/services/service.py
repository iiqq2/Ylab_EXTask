import json
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import producer
from source.api.caches.cache import clear_cache
from source.api.caches.decorators import cache_item_response, cache_list_response
from source.api.factories.factory import RepositoryFactory
from source.api.repositories.interfaces import BaseService
from source.api.schems.schemas import DishScheme, MenuScheme, SubmenuScheme


class MenuService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    @cache_list_response(cache_key='get_menus', ttl=60)
    async def get_all(self) -> JSONResponse:
        repository = await RepositoryFactory.create('menu', self.db)
        menus_list = await repository.get_all()
        return JSONResponse(content=menus_list, status_code=status.HTTP_200_OK)

    @cache_item_response(cache_key_prefix='menu', ttl=60)
    async def get(self, menu_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('menu', self.db)
        menu = await repository.get(menu_id)
        if menu is not None:
            return JSONResponse(content=menu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'menu not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, menu_schema: MenuScheme) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.create(title=menu_schema.title, description=menu_schema.description)

        producer.produce('menu_topic', key=menu_data['id'], value=json.dumps(menu_data).encode('utf-8'))

        return JSONResponse(content=menu_data, status_code=status.HTTP_201_CREATED)

    async def update(self, menu_id: UUID, menu_schema: MenuScheme) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.update(id=menu_id, title=menu_schema.title, description=menu_schema.description)

        producer.produce('menu_topic', key=str(menu_data['id']), value=json.dumps(menu_data).encode('utf-8'))

        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)

    async def delete(self, menu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.delete(id=menu_id)

        producer.produce('menu_topic', key=str(menu_id), value=None)

        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)


class SubMenuService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    @cache_list_response(cache_key='get_submenus', ttl=60)
    async def get_all(self) -> JSONResponse:
        repository = await RepositoryFactory.create('submenu', self.db)
        submenus_list = await repository.get_all()
        return JSONResponse(content=submenus_list, status_code=status.HTTP_200_OK)

    @cache_item_response(cache_key_prefix='submenu', ttl=60)
    async def get(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu = await repository.get(menu_id=menu_id, id=submenu_id)
        if submenu is not None:
            return JSONResponse(content=submenu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, menu_id: UUID, submenu_schema: SubmenuScheme) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.create(menu_id=menu_id, title=submenu_schema.title,
                                               description=submenu_schema.description)

        producer.produce('submenu_topic', key=str(submenu_data['id']), value=json.dumps(submenu_data).encode('utf-8'))

        return JSONResponse(content=submenu_data, status_code=status.HTTP_201_CREATED)

    async def update(self, submenu_id: UUID, submenu_schema: SubmenuScheme) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.update(id=submenu_id, title=submenu_schema.title,
                                               description=submenu_schema.description)

        producer.produce('submenu_topic', key=str(submenu_data['id']), value=json.dumps(submenu_data).encode('utf-8'))

        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)

    async def delete(self, submenu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.delete(submenu_id)

        producer.produce('submenu_topic', key=str(submenu_id), value=None)

        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)


class DishService(BaseService):

    def __init__(self, db: AsyncSession):
        self.db = db

    @cache_list_response(cache_key='get_dishes', ttl=60)
    async def get_all(self) -> JSONResponse:
        repository = await RepositoryFactory.create('dish', self.db)
        dishes_list = await repository.get_all()
        return JSONResponse(content=dishes_list, status_code=status.HTTP_200_OK)

    @cache_item_response(cache_key_prefix='dish', ttl=60)
    async def get(self, dish_id: UUID, submenu_id: UUID) -> JSONResponse:
        repository = await RepositoryFactory.create('dish', self.db)
        dish = await repository.get(dish_id=dish_id, submenu_id=submenu_id)
        if dish is not None:
            return JSONResponse(content=dish, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'dish not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, dish_schema: DishScheme, submenu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.create(submenu_id=submenu_id, title=dish_schema.title,
                                            price=dish_schema.price, description=dish_schema.description)

        producer.produce('dish_topic', key=str(dish_data['id']), value=json.dumps(dish_data).encode('utf-8'))

        return JSONResponse(content=dish_data, status_code=status.HTTP_201_CREATED)

    async def update(self, dish_id: UUID, dish_schema: DishScheme) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.update(title=dish_schema.title, price=dish_schema.price,
                                            description=dish_schema.description, id=dish_id)

        producer.produce('dish_topic', key=str(dish_data['id']), value=json.dumps(dish_data).encode('utf-8'))

        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)

    async def delete(self, dish_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.delete(dish_id)

        producer.produce('dish_topic', key=str(dish_data['id']), value=None)

        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)
