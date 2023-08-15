from sqlalchemy.orm import Session

from source.api.repositories.interfaces import BaseRepository
from source.api.repositories.repository import (
    DishRepository,
    MenuRepository,
    SubMenuRepository,
)


class RepositoryFactory:
    repositories: dict[str, type[BaseRepository]] = {'menu': MenuRepository,
                                                     'submenu': SubMenuRepository, 'dish': DishRepository}

    @classmethod
    async def create(cls, name: str, db: Session) -> BaseRepository:
        if name in cls.repositories:
            return cls.repositories[name](db)
        raise ValueError('Repository not found: %s' % name)
