"""для генерации случайных id"""
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()
class Order(BaseModel):
    """класс заказов пользователя"""
    user_id: str = None
    order_id: str = uuid.uuid4().hex
    price: int = None
    delivery_date: str = None
    number_of_items:int = 0

class Item(BaseModel):
    """класс предметов заказа"""
    name: str = None
    item_id: str = uuid.uuid4().hex
    order_id: str = None
    price: int = None

items = []
orders = []

@app.get("/orders")
async def get_orders():
    """возвращает список всех заказов"""
    return orders

@app.get("/items")
async def get_items():
    """возвращает список всех предметов"""
    return items


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """возвращает заказ по id"""
    for i in orders:
        if i.order_id == order_id:
            return i
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """возвращает предмет по id"""
    for i in items:
        if i.item_id == item_id:
            return i
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.post("/items")
async def create_item(item: Item):
    """создает предмет"""
    items.append(item)
    return items

@app.post("/orders")
async def create_order(order: Order):
    """создает заказ"""
    orders.append(order)
    return orders

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    """изменяет поля предмета по id"""
    for i, preitem in enumerate(items):
        if preitem.item_id == item_id:
            items[i] = item
            return {"status": "200"}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.put("/orders/{order_id}")
async def update_order(order_id: str, order: Order):
    """изменяет поля заказа по id"""
    for i, preorder in enumerate(orders):
        if preorder.order_id == order_id:
            orders[i] = order
            return {"status": "200"}
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    """удаляет заказ по id"""
    for i, order in enumerate(orders):
        if order.order_id == order_id:
            orders.pop(i)
            return {"status": "200"}
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """удаляет предмет по id"""
    for i, item in enumerate(items):
        if item.item_id == item_id:
            items.pop(i)
            return {"status": "200"}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.get("/users/{user_id}")
async def get_users_orders(user_id: str):
    """возвращает заказы по id пользователя которому принадлежит эти заказы"""
    orders_of_user = []
    for i in orders:
        if i.user_id == user_id:
            orders_of_user.append(i)
    return orders_of_user

@app.get("/get_items_of_order/{order_id}")
async def get_orders_items(order_id: str):
    """возвращает предметы заказа по id заказа"""
    items_of_order = []
    for i in items:
        if i.order_id == order_id:
            items_of_order.append(i)
    return items_of_order

def start_server():
    """запускает сервер"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start_server()
