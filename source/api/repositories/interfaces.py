from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from source.db.models import Base


class BaseRepository(ABC):

    def __init__(self, db: Session):
        self.db = db

    @property
    @abstractmethod
    def model(self) -> type[Base]:
        raise NotImplementedError


class BaseService(ABC):
    
    @abstractmethod
    def get_all(self, *args, **kwargs) -> list:
        raise NotImplementedError

    @abstractmethod
    def get(self, *args, **kwargs) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs) -> dict | None:
        raise NotImplementedError
