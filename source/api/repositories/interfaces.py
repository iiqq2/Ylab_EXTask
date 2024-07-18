from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseService(ABC):

    @abstractmethod
    def get_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class BaseRepository(BaseService, ABC):

    def __init__(self, db: Session):
        self.db = db

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError
