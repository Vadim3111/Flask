import datetime

from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    status: str


class Order(BaseModel):
    id: int
    user_id: int
    goods_id: int
    order_date: str
