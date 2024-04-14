from datetime import datetime

import databases
import sqlalchemy as sa
from sqlalchemy import create_engine

from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer,
              primary_key=True),
    sa.Column("username", sa.String(32)),
    sa.Column("email", sa.String(128)),
    sa.Column("password", sa.String(128)),
)

goods = sa.Table(
    'goods',
    metadata,
    sa.Column("id", sa.Integer,
              primary_key=True),
    sa.Column("name", sa.String(32)),
    sa.Column("description", sa.String(256)),
    sa.Column("price", sa.Integer),
)

orders = sa.Table(
    'orders',
    metadata,
    sa.Column("id", sa.Integer,
              primary_key=True),
    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    sa.Column("goods_id", sa.Integer(), sa.ForeignKey("goods.id"), nullable=False),
    sa.Column("order_date", sa.String(64), nullable=False, default=datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
              onupdate=datetime.now().strftime("%d/%m/%y, %H:%M:%S")),
    sa.Column("status", sa.String(64)),
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
