from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from source.api.schems.schemas import SubmenuScheme
from source.api.services.service import SubMenuService
from source.db.database import get_db

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])


@router.get('/list/{skip}/{limit}')
async def get_all_submenu(skip: int, limit: int, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    submenus = SubMenuService(db)
    return await submenus.get_all(skip=skip, limit=limit)


@router.get('/{submenu_id}')
async def get_submenu(submenu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    submenu = SubMenuService(db)
    return await submenu.get(submenu_id=submenu_id)


@router.post('/')
async def create_submenu(menu_id: UUID, submenu_schema: SubmenuScheme, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    submenu = SubMenuService(db)
    return await submenu.create(menu_id=menu_id, submenu_schema=submenu_schema)


@router.patch('/{submenu_id}')
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu_schema: SubmenuScheme, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    submenu = SubMenuService(db)
    return await submenu.update(menu_id=menu_id, submenu_id=submenu_id, submenu_schema=submenu_schema)


@router.delete('/{submenu_id}')
async def delete_submenu(menu_id: UUID, submenu_id: UUID, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    submenu = SubMenuService(db)
    return await submenu.delete(menu_id=menu_id, submenu_id=submenu_id)
