import json
from decimal import Decimal
from uuid import UUID

from easy_profile import SessionProfiler
from sqlalchemy import select

from config import producer
from source.api.repositories.interfaces import BaseRepository
from source.db.models import Dish, Menu, Submenu

profiler = SessionProfiler()


class MenuRepository(BaseRepository):

    model = Menu

    async def get_all(self) -> list[dict[str, str]]:

        res = await self.db.execute(select(self.model))
        menus = res.unique().scalars()
        menus_list = [
            {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus': [
                    {
                        'id': str(submenu.id),
                        'menu_id': str(submenu.menu_id),
                        'title': submenu.title,
                        'description': submenu.description,
                        'dishes': [
                            {
                                'id': str(dish.id),
                                'submenu_id': str(dish.submenu_id),
                                'title': dish.title,
                                'description': dish.description,
                                'price': dish.price
                            }
                            for dish in submenu.dishes
                        ]
                    }
                    for submenu in menu.submenus
                ]
            }
            for menu in menus
        ]
        return menus_list

    async def get(self, menu_id: UUID) -> dict[str, str | int] | None:
        menu = await self.db.get(self.model, menu_id)
        if menu is None:
            return None
        submenus_count = len(menu.submenus)
        dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
        return {'id': str(menu.id), 'title': menu.title, 'description': menu.description, 'dishes_count': dishes_count, 'submenus_count': submenus_count}

    async def create(self, title: str | None, description: str | None) -> dict[str, str]:
        async with self.db.begin():
            menu = self.model(title=title, description=description)
            self.db.add(menu)
            producer.produce('menu_topic', key=str(menu.id), value=json.dumps(
                {'id': str(menu.id), 'title': menu.title, 'description': menu.description}).encode('utf-8'))
        await self.db.refresh(menu)
        return {'id': str(menu.id), 'title': menu.title, 'description': menu.description}

    async def update(self, id: UUID, title: str | None, description: str | None) -> dict[str, str] | None:
        async with self.db.begin():
            menu = await self.db.get(self.model, id)
            if menu is None:
                return None
            if title is not None:
                menu.title = title
            if description is not None:
                menu.description = description
            producer.produce('menu_topic', key=str(menu.id), value=json.dumps(
                {'id': str(menu.id), 'title': menu.title, 'description': menu.description}).encode('utf-8'))
        await self.db.refresh(menu)
        return {'id': str(menu.id), 'title': menu.title, 'description': menu.description}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            menu = await self.db.get(Menu, id)
            if menu is None:
                return None
            await self.db.delete(menu)
            producer.produce('menu_topic', key=str(id), value=None)
        return {'id': str(menu.id), 'title': menu.title, 'description': menu.description}


class SubMenuRepository(BaseRepository):

    model = Submenu

    async def get_all(self) -> list[dict[str, str]]:
        res = await self.db.execute(select(self.model))
        submenus = res.unique().scalars().all()
        submenus_list = [
            {
                'id': str(submenu.id),
                'menu_id': str(submenu.menu_id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes': [
                    {
                        'id': str(dish.id),
                        'submenu_id': str(dish.submenu_id),
                        'title': dish.title,
                        'description': dish.description,
                        'price': dish.price
                    }
                    for dish in submenu.dishes
                ]
            }
            for submenu in submenus
        ]
        return submenus_list

    async def get(self, id: UUID, menu_id: UUID) -> dict[str, str | int] | None:
        stmt = select(self.model).where(self.model.id == id, self.model.menu_id == menu_id)
        result = await self.db.execute(stmt)
        submenu = result.scalar()
        if submenu is None:
            return None
        dishes_count = len(submenu.dishes)
        return {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description, 'dishes_count': dishes_count}

    async def create(self, title: str | None, description: str | None, menu_id: UUID) -> dict[str, str]:
        async with self.db.begin():
            submenu = self.model(title=title, description=description, menu_id=menu_id)
            menu = await self.db.get(Menu, menu_id)
            menu.submenus.append(submenu)
            self.db.add(submenu)
            producer.produce('submenu_topic', key=str(submenu.id), value=json.dumps(
                {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description}).encode('utf-8'))
        await self.db.refresh(submenu)
        return {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description}

    async def update(self, title: str | None, description: str | None, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            submenu = await self.db.get(self.model, id)
            if submenu is None:
                return None
            if title is not None:
                submenu.title = title
            if description is not None:
                submenu.description = description
            producer.produce('submenu_topic', key=str(submenu.id), value=json.dumps(
                {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description}).encode('utf-8'))
        await self.db.refresh(submenu)
        return {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            submenu = await self.db.get(self.model, id)
            if submenu is None:
                return None
            await self.db.delete(submenu)
            producer.produce('submenu_topic', key=str(id), value=None)
        return {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description}


class DishRepository(BaseRepository):

    model = Dish

    async def get_all(self) -> list[dict[str, str]]:
        res = await self.db.execute(select(self.model))
        dishes = res.unique().scalars().all()
        dishes_list = [
            {
                'id': str(dish.id),
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price)
            }
            for dish in dishes
        ]
        return dishes_list

    async def get(self, dish_id: UUID, submenu_id: UUID) -> dict[str, str] | None:
        stmt = select(self.model).where(self.model.id == dish_id, self.model.submenu_id == submenu_id)
        result = await self.db.execute(stmt)
        dish = result.scalar()
        if dish is None:
            return None
        return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}

    async def create(self, title: str | None, price: Decimal | None, description: str | None, submenu_id: UUID) -> dict[str, str]:
        async with self.db.begin():
            dish = self.model(title=title, description=description, price=price, submenu_id=submenu_id)
            submenu = await self.db.get(Submenu, submenu_id)
            submenu.dishes.append(dish)
            self.db.add(dish)
            producer.produce('dish_topic', key=str(dish.id), value=json.dumps(
                {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}).encode('utf-8'))
        await self.db.refresh(dish)
        return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}

    async def update(self, id: UUID, title: str | None, price: Decimal | None, description: str | None) -> dict[str, str] | None:
        async with self.db.begin():
            dish = await self.db.get(self.model, id)
            if dish is None:
                return None
            if title is not None:
                dish.title = title
            if description is not None:
                dish.description = description
            if price is not None:
                dish.price = price
            producer.produce('dish_topic', key=str(dish.id), value=json.dumps(
                {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}).encode('utf-8'))
        await self.db.refresh(dish)
        return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            dish = await self.db.get(self.model, id)
            if dish is None:
                return None
            await self.db.delete(dish)
            producer.produce('dish_topic', key=str(id), value=None)
        return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}
