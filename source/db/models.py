import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'), nullable=False)
    submenu = relationship('Submenu', back_populates='dishes', single_parent=True, lazy='joined')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'), nullable=False)
    menu = relationship('Menu', back_populates='submenus', lazy='joined', single_parent=True)
    dishes = relationship('Dish', back_populates='submenu', lazy='joined', cascade='all, delete-orphan')


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    submenus = relationship('Submenu', back_populates='menu', lazy='joined', cascade='all, delete-orphan')
