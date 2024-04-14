from fastapi import APIRouter
from db import goods, database
from models.goods import Goods, GoodsIn

router = APIRouter()


@router.post("/fake_goods/{count}")
async def create_fake_goods(count: int):
    for i in range(count):
        query = goods.insert().values(name=f'name{i}',
                                      description=f'description{i}',
                                      price=i * 1000)
        await database.execute(query)
    return {'message': f'{count} fake goods create'}


@router.post("/goods", response_model=GoodsIn)
async def create_goods(new_goods: GoodsIn):
    query = goods.insert().values(name=new_goods.name,
                                  description=new_goods.description, price=new_goods.price)
    last_record_id = await database.execute(query)
    return {**new_goods.dict(), "id": last_record_id}


@router.put("/goods/{goods_id}", response_model=Goods)
async def update_goods(goods_id: int, new_goods: GoodsIn):
    query = goods.update().where(goods.c.id == goods_id).values(**new_goods.dict())
    await database.execute(query)
    return {**new_goods.dict(), "id": goods_id}


@router.get("/all_goods/")
async def read_all_goods():
    query = goods.select()
    return await database.fetch_all(query)


@router.get("/goods/{goods_id}", response_model=Goods)
async def read_goods(goods_id: int):
    query = goods.select().where(goods.c.id == goods_id)
    return await database.fetch_one(query)


@router.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int):
    query = goods.delete().where(goods.c.id == goods_id)
    await database.execute(query)
    return {'message': 'Goods deleted'}
