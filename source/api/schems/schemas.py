from decimal import Decimal

from pydantic import BaseModel


class MenuScheme(BaseModel):
    title: str
    description: str


class SubmenuScheme(BaseModel):
    title: str
    description: str


class DishScheme(BaseModel):
    title: str
    description: str
    price: Decimal
