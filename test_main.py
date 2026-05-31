# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app, items, next_id
import app.main as main_module


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory DB before each test."""
    main_module.items.clear()
    main_module.next_id = 1
    yield


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello" in response.json()["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_item():
    response = client.post("/items", json={"name": "Apple", "price": 1.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Apple"
    assert data["price"] == 1.99
    assert "id" in data


def test_get_item():
    # Create first
    client.post("/items", json={"name": "Banana", "price": 0.99})
    # Then retrieve
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Banana"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_list_items():
    client.post("/items", json={"name": "Cherry", "price": 3.50})
    client.post("/items", json={"name": "Date", "price": 5.00})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


def test_delete_item():
    client.post("/items", json={"name": "Elderberry", "price": 8.00})
    response = client.delete("/items/1")
    assert response.status_code == 200
    # Confirm it's gone
    assert client.get("/items/1").status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404
