from fastapi.responses import JSONResponse
import json
from source.api.factories.factory import RepositoryFactory
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import status
from source.api.caches.cache import clear_cache, get_cache_data, create_cache_data
from source.api.schems.schemas import MenuCreate, SubMenuCreate, DishCreate, DishUpdate
from source.api.repositories.interfaces import BaseHandler


class MenuHandler(BaseHandler):
    
    def __init__(self,db: AsyncSession):
        self.db = db
    
    async def get_all(self) -> JSONResponse:
        cache_data = await get_cache_data('get_menus')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('menu', self.db)
        menus_list = await repository.get_all()
        await create_cache_data(url='get_menus', time=60, object=json.dumps(menus_list))
        return JSONResponse(content=menus_list, status_code=status.HTTP_200_OK)
    
    async def get(self, menu_id: UUID) -> JSONResponse:
        cache_data = await get_cache_data(f'get_menu_{menu_id}')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('menu', self.db)
        menu = await repository.get(menu_id)
        if menu is not None:
            await create_cache_data(url=f'get_menu_{menu_id}', time=60, object=JSONResponse(content=menu).body)
            return JSONResponse(content=menu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'menu not found'}, status_code=status.HTTP_404_NOT_FOUND)
    
    async def create(self, menu_schema: MenuCreate) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.create(title=menu_schema.title, description=menu_schema.description)
        return JSONResponse(content=menu_data, status_code=status.HTTP_201_CREATED)
    
    async def delete(self, menu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.delete(id=menu_id)
        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)
    
    async def update(self, menu_id: UUID, menu_schema: MenuCreate) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('menu', self.db)
        menu_data = await repository.update(id=menu_id, title=menu_schema.title, description=menu_schema.description)
        return JSONResponse(content=menu_data, status_code=status.HTTP_200_OK)
    
class SubMenuHandler(BaseHandler):
    
    def __init__(self,db: AsyncSession):
        self.db = db

    async def get_all(self) -> JSONResponse:
        cache_data = await get_cache_data('get_submenus')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('submenu', self.db)
        submenus_list = await repository.get_all()
        await create_cache_data(url='get_submenus', time=60, object=json.dumps(submenus_list))
        return JSONResponse(content=submenus_list, status_code=status.HTTP_200_OK)
    
    async def get(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        cache_data = await get_cache_data(f'get_submenu_{submenu_id}')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu = await repository.get(menu_id=menu_id, id=submenu_id)
        if submenu is not None:
            await create_cache_data(url=f'get_submenu_{submenu_id}', time=60, object=JSONResponse(content=submenu).body)
            return JSONResponse(content=submenu, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=status.HTTP_404_NOT_FOUND)
    
    async def create(self, menu_id: UUID, submenu_schema: SubMenuCreate) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.create(menu_id=menu_id, title=submenu_schema.title,
                                        description=submenu_schema.description)
        return JSONResponse(content=submenu_data, status_code=status.HTTP_201_CREATED)
    
    async def update(self, submenu_id: UUID, submenu_schema: SubMenuCreate) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.update(id=submenu_id, title=submenu_schema.title,
                                        description=submenu_schema.description)
        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)
    
    async def delete(self, submenu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('submenu', self.db)
        submenu_data = await repository.delete(submenu_id)
        return JSONResponse(content=submenu_data, status_code=status.HTTP_200_OK)

class DishHandler(BaseHandler):

    def __init__(self,db: AsyncSession):
        self.db = db

    async def get_all(self) -> JSONResponse:
        cache_data = await get_cache_data('get_dishes')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('dish', self.db)
        dishes_list = await repository.get_all()
        await create_cache_data(url='get_dishes', time=60, object=json.dumps(dishes_list))
        return JSONResponse(content=dishes_list, status_code=status.HTTP_200_OK)

    async def get(self, dish_id: UUID, submenu_id: UUID) -> JSONResponse:
        cache_data = await get_cache_data(f'get_dish_{dish_id}')
        if cache_data:
            return json.loads(cache_data)
        repository = await RepositoryFactory.create('dish', self.db)
        dish = await repository.get(dish_id=dish_id, submenu_id=submenu_id)
        if dish is not None:
            await create_cache_data(url=f'get_dish_{dish_id}', time=60, object=JSONResponse(content=dish).body)
            return JSONResponse(content=dish, status_code=status.HTTP_200_OK)
        return JSONResponse(content={'detail': 'dish not found'}, status_code=status.HTTP_404_NOT_FOUND)

    async def create(self, dish_schema: DishCreate, submenu_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.create(submenu_id=submenu_id, title=dish_schema.title,
                                    price=dish_schema.price, description=dish_schema.description)
        return JSONResponse(content=dish_data, status_code=status.HTTP_201_CREATED)

    async def update(self, dish_id: UUID, dish_schema: DishUpdate) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.update(title=dish_schema.title, price=dish_schema.price,
                                    description=dish_schema.description, id=dish_id)
        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)

    async def delete(self, dish_id: UUID) -> JSONResponse:
        await clear_cache()
        repository = await RepositoryFactory.create('dish', self.db)
        dish_data = await repository.delete(dish_id)
        return JSONResponse(content=dish_data, status_code=status.HTTP_200_OK)
