from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from source.api.handlers.handler import MenuHandler
from source.api.schems.schemas import MenuCreate
from source.db.database import get_db

router = APIRouter(prefix='/api/v1/menus', tags=['Menus'])


@router.get('/')
async def get_menus(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    menus_list = MenuHandler(db)
    return await menus_list.get_all()


@router.post('/')
async def create_menu(menu_schema: MenuCreate, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    menu = MenuHandler(db)
    return await menu.create(menu_schema)


@router.get('/{menu_id}')
async def get_menu(menu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    menu = MenuHandler(db)
    return await menu.get(menu_id)


@router.delete('/{menu_id}')
async def delete_menu(menu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    menu = MenuHandler(db)
    return await menu.delete(menu_id)


@router.patch('/{menu_id}')
async def update_menu(menu_id: UUID, menu_schema: MenuCreate, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    menu = MenuHandler(db)
    return await menu.update(menu_id=menu_id, menu_schema=menu_schema)
