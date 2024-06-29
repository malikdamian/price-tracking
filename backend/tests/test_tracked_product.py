from fastapi.testclient import TestClient

from backend.database import TrackedProducts


def test_add_tracked_product(client: TestClient) -> None:
    response = client.post("/tracked-products", params={"name": "Test"})

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Tracked product added successfully"
    assert data["id"] == 1


def test_toggle_tracked_product(client: TestClient, tracked_product: TrackedProducts) -> None:
    response = client.patch("/tracked-products/1")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Tracked product toggled successfully"


def test_toggle_tracked_product_not_found(client: TestClient) -> None:
    response = client.patch("/tracked-products/23121")

    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data["detail"] == "Tracked product not found."


def test_get_tracked_products(client: TestClient, tracked_product: TrackedProducts) -> None:
    response = client.get("/tracked-products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    product = data[0]
    assert product["id"] == 1
    assert product["name"] == "Test product"
    assert product["tracked"] is True
