import json
from decimal import Decimal
from uuid import UUID

from easy_profile import SessionProfiler
from sqlalchemy import delete, func, insert, select, text, update

from config import producer
from source.api.repositories.interfaces import BaseRepository
from source.db.models import Dish, Menu, Submenu

profiler = SessionProfiler()


class MenuRepository(BaseRepository):

    model = Menu

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:

        res = await self.db.execute(text('''
            SELECT
                cast(menus.id as text) AS menu_id,
                menus.title AS menu_title,
                menus.description AS menu_description,
                COALESCE(
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'submenu_id', cast(submenus.id as text),
                            'submenu_title', submenus.title,
                            'dishes', COALESCE(submenus_dishes.dishes, '[]'::json)
                        )
                    ) FILTER (WHERE submenus.id IS NOT NULL),
                    '[]'::json
                ) AS submenus
            FROM menus
            LEFT JOIN submenus ON menus.id = submenus.menu_id
            LEFT JOIN (
                SELECT
                    dishes.submenu_id,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'dish_id', cast(dishes.id as text),
                            'dish_title', dishes.title,
                            'dish_price', dishes.price
                        )
                    ) AS dishes
                FROM dishes
                GROUP BY dishes.submenu_id
            ) AS submenus_dishes ON submenus.id = submenus_dishes.submenu_id
            GROUP BY menus.id
            ORDER BY menus.id
            LIMIT :limit
            OFFSET :skip;
            '''), {'limit': limit, 'skip': skip})

        rows = res.mappings().all()
        return [
            {
                'id': row.menu_id,
                'title': row.menu_title,
                'description': row.menu_description,
                'submenus': row.submenus
            }
            for row in rows
        ]

    async def get(self, menu_id: UUID) -> dict[str, str | int] | None:

        res = await self.db.execute(text(
            '''
            select menus.id, menus.description, menus.title, count(distinct submenus.id) as submenus_count, count(distinct dishes.id) as dishes_count from menus
            LEFT JOIN submenus ON menus.id = submenus.menu_id
            LEFT JOIN dishes ON submenus.id = dishes.submenu_id
            where menus.id = :id
            group by menus.id
            ORDER BY menus.id'''
        ), {'id': menu_id})
        menu_data = res.mappings().fetchone()

        if menu_data:
            return {
                'id': str(menu_data.id),
                'title': menu_data.title,
                'description': menu_data.description,
                'submenus_count': menu_data.submenus_count,
                'dishes_count': menu_data.dishes_count
            }

    async def create(self, title: str, description: str) -> dict[str, str]:
        stmt = text('''
        WITH first_insert AS (
            INSERT INTO menus (title, description)
            VALUES (:title, :description)
            RETURNING id, title, description
        )
        INSERT INTO deferred_tasks (topic, key, value, created_at)
        SELECT
            'menu_topic' AS topic,
            id AS key,
            json_build_object('action', 'create','menu_id', id, 'title', title, 'description', description) AS value,
            now() as created_at

        FROM first_insert
        RETURNING value->>'menu_id' as menu_id
        ''')
        async with self.db.begin():
            res = await self.db.execute(stmt, {'title': title, 'description': description})
        new_menu_id = res.mappings().fetchone()['menu_id']
        return {'id': str(new_menu_id), 'title': title, 'description': description}

    async def update(self, id: UUID, title: str | None, description: str | None) -> dict[str, str] | None:
        stmt = text('''
        WITH updated_menu AS (
        UPDATE menus
        SET
            title = :title,
            description = :description
        WHERE id = :id
        RETURNING id, title, description
        )
        INSERT INTO deferred_tasks (topic, key, value, created_at)
        SELECT
            'menu_topic' AS topic,
            updated_menu.id AS key,
            json_build_object(
                'action', 'update',
                'menu_id', updated_menu.id,
                'title', updated_menu.title,
                'description', updated_menu.description
            ) AS value,
            now() as created_at
        FROM updated_menu
        RETURNING value
        ''')
        async with self.db.begin():
            res = await self.db.execute(stmt, {'id': id, 'title': title, 'description': description})
        updated_values = res.mappings().fetchone()['value']

        return {'id': updated_values['menu_id'], 'title': updated_values['title'], 'description': updated_values['description']}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        stmt = text('''
        with deleted_menu as (delete from menus where id = :id returning id, title, description)
        insert into deferred_tasks (topic, key, value, created_at)
        select
            'menu_topic' as topic,
            deleted_menu.id as key,
            json_build_object(
                'action', 'delete',
                'menu_id', deleted_menu.id,
                'title', deleted_menu.title,
                'description', deleted_menu.description
            ) AS value,
            now() AS created_at
        from deleted_menu
        returning value
        ''')
        async with self.db.begin():
            res = await self.db.execute(stmt, {'id': id})
        deleted_values = res.mappings().fetchone()['value']

        return {'id': deleted_values['menu_id'], 'title': deleted_values['title'], 'description': deleted_values['description']}


class SubMenuRepository(BaseRepository):

    model = Submenu

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:
        stmt = select(self.model, Dish).outerjoin(Dish, self.model.id ==
                                                  Dish.submenu_id).order_by(self.model.id).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        submenu_rows = res.scalars().unique().all()

        return [
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
            } for submenu in submenu_rows
        ]

    async def get(self, id: UUID) -> dict[str, str | int] | None:
        stmt = select(self.model, func.count(Dish.id)).where(self.model.id == id).outerjoin(
            Dish, id == Dish.submenu_id).group_by(self.model.id)
        _ = await self.db.execute(stmt)
        res = _.unique().fetchall()

        if res:
            submenu, dishes_count = res[0]
            return {
                'id': str(id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': dishes_count
            }

    async def create(self, title: str, description: str, menu_id: UUID) -> dict[str, str]:
        async with self.db.begin():
            stmt = insert(self.model).values(title=title, description=description,
                                             menu_id=menu_id).returning(self.model.id)
            res = await self.db.execute(stmt)
            new_submenu_id = str(res.scalar_one())
            producer.produce('submenu_topic', key=new_submenu_id, value=json.dumps(
                {'id': new_submenu_id, 'title': title, 'description': description}).encode('utf-8'))
        return {'id': new_submenu_id, 'title': title, 'description': description}

    async def update(self, title: str | None, description: str | None, id: UUID) -> dict[str, str] | None:
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
            producer.produce('submenu_topic', key=str(id), value=json.dumps(
                {'id': str(id), 'title': updated_values.title, 'description': updated_values.description}).encode('utf-8'))
        return {'id': str(id), 'title': updated_values.title, 'description': updated_values.description}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            stmt = delete(self.model).where(self.model.id == id).returning(self.model.title, self.model.description)
            res = await self.db.execute(stmt)
            deleted_values = res.fetchone()
            producer.produce('submenu_topic', key=str(id), value=None)
        return {'id': str(id), 'title': deleted_values.title, 'description': deleted_values.description}


class DishRepository(BaseRepository):

    model = Dish

    async def get_all(self, skip: int, limit: int) -> list[dict[str, str]]:
        stmt = select(self.model).order_by(self.model.id).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        dishes_rows = res.scalars().unique().all()
        return [
            {
                'id': str(dish.id),
                'submenu_id': str(dish.submenu_id),
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price)
            }
            for dish in dishes_rows
        ]

    async def get(self, dish_id: UUID) -> dict[str, str] | None:
        stmt = select(self.model).where(self.model.id == dish_id)
        res = await self.db.execute(stmt)
        dish = res.unique().scalar_one_or_none()
        print(dish)
        if dish:
            return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}

    async def create(self, title: str, price: Decimal, description: str, submenu_id: UUID) -> dict[str, str]:
        async with self.db.begin():
            stmt = insert(self.model).values(title=title, price=price, description=description,
                                             submenu_id=submenu_id).returning(self.model.id)
            res = await self.db.execute(stmt)
            new_dish_id = str(res.scalar_one())
            producer.produce('dish_topic', key=new_dish_id, value=json.dumps(
                {'id': new_dish_id, 'title': title, 'description': description, 'price': str(price)}).encode('utf-8'))
        return {'id': new_dish_id, 'title': title, 'description': description, 'price': str(price)}

    async def update(self, id: UUID, title: str | None, price: Decimal | None, description: str | None) -> dict[str, str] | None:
        async with self.db.begin():
            values = {}
            if title:
                values['title'] = title
            if description:
                values['description'] = description
            if price:
                values['price'] = price
            if values:
                stmt = update(self.model).where(self.model.id == id).values(
                    **values).returning(self.model.title, self.model.description, self.model.price)
                res = await self.db.execute(stmt)
                updated_values = res.fetchone()
            producer.produce('dish_topic', key=str(id), value=json.dumps(
                {'id': str(id), 'title': updated_values.title, 'description': updated_values.description, 'price': str(updated_values.price)}).encode('utf-8'))
        return {'id': str(id), 'title': updated_values.title, 'description': updated_values.description, 'price': str(updated_values.price)}

    async def delete(self, id: UUID) -> dict[str, str] | None:
        async with self.db.begin():
            stmt = delete(self.model).where(self.model.id == id).returning(
                self.model.title, self.model.description, self.model.price)
            res = await self.db.execute(stmt)
            deleted_values = res.fetchone()
            producer.produce('dish_topic', key=str(id), value=None)
        return {'id': str(id), 'title': deleted_values.title, 'description': deleted_values.description, 'price': str(deleted_values.price)}
