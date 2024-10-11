import json
from decimal import Decimal
from uuid import UUID

from easy_profile import SessionProfiler
from sqlalchemy import delete, func, insert, outerjoin, select, update

from config import producer
from source.api.repositories.interfaces import BaseRepository
from source.db.models import Dish, Menu, Submenu

profiler = SessionProfiler()


class MenuRepository(BaseRepository):

    model = Menu

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:

        stmt = select(self.model, Submenu, Dish).select_from(
            outerjoin(self.model, Submenu, self.model.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        ).order_by(self.model.id).offset(skip).limit(limit)

        res = await self.db.execute(stmt)
        menu_rows = res.scalars().unique().all()

        return [
            {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus': [
                    {
                        'id': str(submenu.id),
                        'title': submenu.title,
                        'description': submenu.description,
                        'dishes': [
                            {
                                'id': str(dish.id),
                                'title': dish.title,
                                'description': dish.description,
                                'price': str(dish.price)
                            } for dish in submenu.dishes
                        ]
                    } for submenu in menu.submenus
                ]
            } for menu in menu_rows
        ]

    async def get(self, menu_id: UUID) -> dict[str, str | int] | None:

        stmt = select(self.model, func.count(Submenu.id), func.count(Dish.id)).where(self.model.id == menu_id).select_from(
            outerjoin(self.model, Submenu, menu_id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        ).group_by(self.model.id)

        _ = await self.db.execute(stmt)
        res = _.unique().fetchall()

        if res:
            menu, submenus_count, dishes_count = res[0]
            return {
                'id': str(menu_id),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': submenus_count,
                'dishes_count': dishes_count
            }

    async def create(self, title: str, description: str) -> dict[str, str]:
        async with self.db.begin():
            stmt = insert(self.model).values(title=title, description=description).returning(self.model.id)
            res = await self.db.execute(stmt)
            new_menu_id = str(res.scalar_one())
            producer.produce('menu_topic', key=new_menu_id, value=json.dumps(
                {'id': new_menu_id, 'title': title, 'description': description}).encode('utf-8'))
        return {'id': new_menu_id, 'title': title, 'description': description}

    async def update(self, id: UUID, title: str | None, description: str | None) -> dict[str, str] | None:
        async with self.db.begin():
            values = {}
            if title:
                values['title'] = title
            if description:
                values['description'] = description
            if values:
                stmt = update(self.model).where(self.model.id == id).values(
                    **values).returning(self.model.title, self.model.description)
                res = await self.db.execute(stmt)
                updated_values = res.fetchone()
            producer.produce('menu_topic', key=str(id), value=json.dumps(
                {'id': str(id), 'title': updated_values.title, 'description': updated_values.description}).encode('utf-8'))
        return {'id': str(id), 'title': updated_values.title, 'description': updated_values.description}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.title, self.model.description)
            res = await self.db.execute(stmt)
            deleted_values = res.fetchone()
            producer.produce('menu_topic', key=str(id), value=None)
        return {'id': str(id), 'title': deleted_values.title, 'description': deleted_values.description}


class SubMenuRepository(BaseRepository):

    model = Submenu

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:
        res = await self.db.execute(select(self.model).order_by(self.model.id).offset(skip).limit(limit))
        submenus = res.unique().scalars().all()
        submenus_list = [
            {
                'id': str(submenu.id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes': [
                    {
                        'id': str(dish.id),
                        'title': dish.title,
                        'description': dish.description,
                        'price': str(dish.price)
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
            self.db.add(submenu)
            await self.db.flush()
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
            await self.db.flush()
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

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:
        res = await self.db.execute(select(self.model).order_by(self.model.id).offset(skip).limit(limit))
        dishes = res.unique().scalars().all()
        dishes_list = [
            {
                'id': str(dish.id),
                'submenu_id': str(dish.submenu_id),
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
            self.db.add(dish)
            await self.db.flush()
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
            await self.db.flush()
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
