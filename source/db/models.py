import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(30, 28), nullable=False)
    description: Mapped[str]
    submenu_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey('submenus.id'), nullable=False)
    submenu: Mapped['Submenu'] = relationship('Submenu', back_populates='dishes', single_parent=True, lazy='joined')


class Submenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    menu_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey('menus.id'), nullable=False)
    menu: Mapped['Menu'] = relationship('Menu', back_populates='submenus', lazy='joined', single_parent=True)
    dishes: Mapped[list['Dish']] = relationship(
        'Dish', back_populates='submenu', lazy='joined', cascade='all, delete-orphan')


class Menu(Base):
    __tablename__ = 'menus'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    submenus: Mapped[list['Submenu']] = relationship(
        'Submenu', back_populates='menu', lazy='joined', cascade='all, delete-orphan')


class Outbox(Base):
    __tablename__ = 'deferred_tasks'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, autoincrement=True)
    topic: Mapped[str] = mapped_column(nullable=False)
    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
