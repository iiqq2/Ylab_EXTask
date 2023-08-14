from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from source.api.handlers.handler import DishHandler
from source.api.schems.schemas import DishCreate
from source.db.database import get_db

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.get('/')
async def get_all_dishes(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    dishes = DishHandler(db)
    return await dishes.get_all()


@router.get('/{dish_id}')
async def get_dish(dish_id: UUID, submenu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    dish = DishHandler(db)
    return await dish.get(dish_id=dish_id, submenu_id=submenu_id)


@router.post('/')
async def create_dish(dish_schema: DishCreate, submenu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    dish = DishHandler(db)
    return await dish.create(dish_schema=dish_schema, submenu_id=submenu_id)


@router.patch('/{dish_id}')
async def update_dish(dish_id: UUID, dish_schema: DishCreate, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    dish = DishHandler(db)
    return await dish.update(dish_schema=dish_schema, dish_id=dish_id)


@router.delete('/{dish_id}')
async def delete_dish(dish_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    dish = DishHandler(db)
    return await dish.delete(dish_id)
