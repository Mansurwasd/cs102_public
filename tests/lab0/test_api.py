"""модуль для отправки запросов в api"""

from fastapi.testclient import TestClient
from src.lab0.restfull_api import app

client = TestClient(app)

def test_can_get_orders():
    """тест, возвращяет ли список заказов"""
    responce = client.get("/orders")
    assert responce.status_code == 200

def test_can_get_items():
    """тест, возвращяет ли список предметов"""
    responce = client.get("/items")
    assert responce.status_code == 200

def create_new_order_pattern(user_id, test_id):
    """шаблон заказа для тестов"""
    return {
        "userId": user_id,
        "orderId": test_id,
        "totalPriceCents": 100,
        "placingDate": "25.10.2007",
        "items": [
            {
                "cartItemId": "1",
                "deliveryDate": "27.10.2007",
                "quantity": 2
            },
            {
                "cartItemId": "2",
                "deliveryDate": "29.10.2007",
                "quantity": 1
            }
        ]
    }

def create_new_item_pattern(test_id):
    """шаблон предмета для тестов"""
    return {
        "itemId": test_id,
        "image": "test_path",
        "name": "test_name",
        "rating": {
            "stars": 4.5,
            "count": 87
        },
        "priceCents": 1000,
        "keywords": ["socks", "sports", "apparel"],
        "type": "clothing",
        "sizeChartLink": "images/clothing-size-chart.png"

    }

def test_can_create_order():
    """тест, может ли создать заказ"""
    user_id = "321"
    test_id = "123"
    order = create_new_order_pattern(user_id, test_id)
    post_responce = client.post("/orders", json=order)
    assert post_responce.status_code == 200
    get_responce = client.get("/orders/" + test_id)
    assert get_responce.status_code == 200
    assert get_responce.json() == order
    delete_responce = client.delete("/orders/" + test_id)
    assert delete_responce.status_code == 200

def test_can_create_item():
    """тест, может ли создать предмет"""
    test_id = "321"
    item = create_new_item_pattern(test_id)
    post_responce = client.post("/items", json=[item])
    assert post_responce.status_code == 200
    get_responce = client.get("/items/" + test_id)
    assert get_responce.status_code == 200
    assert get_responce.json() == item
    delete_responce = client.delete("/items/" + test_id)
    assert delete_responce.status_code == 200

def test_can_change_order():
    """тест, может ли изменить поля заказа"""
    user_id = "321"
    test_id = "123"
    order = create_new_order_pattern(user_id, test_id)
    new_order = {
        "userId": order["userId"],
        "orderId": order["orderId"],
        "totalPriceCents": 200,
        "placingDate": "30.10.2007",
        "items": [
            {
                "cartItemId": "6",
                "deliveryDate": "1.11.2007",
                "quantity": 3
            },
            {
                "cartItemId": "7",
                "deliveryDate": "3.11.2007",
                "quantity": 1
            },
        ]
    }
    post_responce = client.post("/orders", json=order)
    assert post_responce.status_code == 200
    put_responce = client.put("/orders/" + test_id, json=new_order)
    assert put_responce.status_code == 200
    get_responce = client.get("/orders/" + test_id)
    assert get_responce.status_code == 200
    assert get_responce.json() == new_order
    delete_responce = client.delete("/orders/" + test_id)
    assert delete_responce.status_code == 200

def test_can_change_item():
    """тест, может ли изменить поля предмета"""
    test_id = "123"
    item = create_new_item_pattern(test_id)
    new_item = {
        "itemId": item["itemId"],
        "image": "test_path",
        "name": "test_name",
        "rating": {
            "stars": 4.6,
            "count": 90
        },
        "priceCents": 1200,
        "keywords": ["mango", "mustard", "67"],
    }
    post_responce = client.post("/items", json=[item])
    assert post_responce.status_code == 200
    put_responce = client.put("/items/" + test_id, json=new_item)
    assert put_responce.status_code == 200
    get_responce = client.get("/items/" + test_id)
    assert get_responce.status_code == 200
    assert get_responce.json() == new_item
    delete_responce = client.delete("/items/" + test_id)
    assert delete_responce.status_code == 200

def test_can_get_orders_of_user():
    """тест, может ли найти все заказы определенного пользователя"""
    user_id = "321"
    test_id = "123"
    second_test_id = "1"
    third_test_id = "2"
    second_user_id = "1"
    order1 = create_new_order_pattern(user_id, test_id)
    order2 = create_new_order_pattern(user_id, second_test_id)
    order3 = create_new_order_pattern(second_user_id, third_test_id)
    post_responce1 = client.post("/orders", json=order1)
    assert post_responce1.status_code == 200
    post_responce2 = client.post("/orders", json=order2)
    assert post_responce2.status_code == 200
    post_responce3 = client.post("/orders", json=order3)
    assert post_responce3.status_code == 200
    get_responce = client.get("/users/" + user_id)
    assert get_responce.status_code == 200
    assert len(get_responce.json()) == 2
    assert get_responce.json()[0] == order1
    assert get_responce.json()[1] == order2
    delete_responce1 = client.delete("/orders/" + test_id)
    assert delete_responce1.status_code == 200
    delete_responce2 = client.delete("/orders/" + second_test_id)
    assert delete_responce2.status_code == 200
    delete_responce3 = client.delete("/orders/" + third_test_id)
    assert delete_responce3.status_code == 200
