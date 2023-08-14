from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str


class SubMenuCreate(BaseModel):
    title: str
    description: str


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class DishUpdate(BaseModel):
    title: str
    description: str
    price: float
