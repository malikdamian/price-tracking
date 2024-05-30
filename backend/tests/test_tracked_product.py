from starlette.testclient import TestClient


def test_add_tracked_product(client: TestClient) -> None:
    response = client.post("/add-tracked-product", params={"name": "Test"})

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Tracked product added successfully"
    assert data["id"] == 1
