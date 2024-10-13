import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(30, 28), nullable=False)
    description: Mapped[str]
    submenu_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey('submenus.id'), nullable=False)
    submenu: Mapped['Submenu'] = relationship('Submenu', back_populates='dishes', single_parent=True)


class Submenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    menu_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey('menus.id'), nullable=False)
    menu: Mapped['Menu'] = relationship('Menu', back_populates='submenus', single_parent=True)
    dishes: Mapped[list['Dish']] = relationship(
        'Dish', back_populates='submenu', cascade='all, delete-orphan')


class Menu(Base):
    __tablename__ = 'menus'

    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    submenus: Mapped[list['Submenu']] = relationship(
        'Submenu', back_populates='menu', cascade='all, delete-orphan')
