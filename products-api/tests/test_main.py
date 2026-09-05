from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_list_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_product():
    payload = {"name": "Widget", "price": 9.99, "stock": 10, "category": "misc"}
    created = client.post("/products", json=payload)
    assert created.status_code == 201
    product_id = created.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Widget"

def test_get_product_not_found():
    response = client.get("/products/nonexistent")
    assert response.status_code == 404
