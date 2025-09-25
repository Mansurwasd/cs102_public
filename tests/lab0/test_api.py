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
        "user_id": user_id,
        "order_id": test_id,
        "price": 100,
        "delivery_date": "25.10.2007",
        "number_of_items": 2
    }

def create_new_item_pattern(order_id, test_id):
    """шаблон предмета для тестов"""
    return {
        "name": "basketball",
        "item_id": test_id,
        "order_id": order_id,
        "price": 100
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
    order_id = "123"
    test_id = "321"
    item = create_new_item_pattern(order_id, test_id)
    post_responce = client.post("/items", json=item)
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
        "user_id": order["user_id"],
        "order_id": order["order_id"],
        "price": 100,
        "delivery_date": "25.10.2007",
        "number_of_items": 3
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
    order_id = "321"
    test_id = "123"
    item = create_new_item_pattern(order_id, test_id)
    new_item = {
        "name": "basketball",
        "item_id": item["item_id"],
        "order_id": item["order_id"],
        "price": 120
    }
    post_responce = client.post("/items", json=item)
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

def test_can_get_items_of_order():
    """тест, может ли найти все предметы определенного заказа"""
    order_id = "321"
    test_id = "123"
    second_test_id = "1"
    third_test_id = "2"
    second_user_id = "1"
    item1 = create_new_item_pattern(order_id, test_id)
    item2 = create_new_item_pattern(order_id, second_test_id)
    item3 = create_new_item_pattern(second_user_id, third_test_id)
    post_responce1 = client.post("/items", json=item1)
    assert post_responce1.status_code == 200
    post_responce2 = client.post("/items", json=item2)
    assert post_responce2.status_code == 200
    post_responce3 = client.post("/items", json=item3)
    assert post_responce3.status_code == 200
    get_responce = client.get("/get_items_of_order/" + order_id)
    assert get_responce.status_code == 200
    assert len(get_responce.json()) == 2
    assert get_responce.json()[0] == item1
    assert get_responce.json()[1] == item2
    delete_responce1 = client.delete("/items/" + test_id)
    assert delete_responce1.status_code == 200
    delete_responce2 = client.delete("/items/" + second_test_id)
    assert delete_responce2.status_code == 200
    delete_responce3 = client.delete("/items/" + third_test_id)
    assert delete_responce3.status_code == 200
