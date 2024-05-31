from fastapi.testclient import TestClient

from backend.database import TrackedProducts


def test_add_tracked_product(client: TestClient) -> None:
    response = client.post("/tracked-product", params={"name": "Test"})

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Tracked product added successfully"
    assert data["id"] == 1


def test_toggle_tracked_product(client: TestClient, tracked_product: TrackedProducts) -> None:
    response = client.patch("/tracked-product/1")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Tracked product toggled successfully"


def test_toggle_tracked_product_not_found(client: TestClient) -> None:
    response = client.patch("/tracked-product/23121")

    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data["detail"] == "Tracked product not found."
