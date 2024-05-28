from fastapi.testclient import TestClient

from backend.database import ProductResult


def test_submit_product_result(client: TestClient) -> None:
    payload = {
        "search_text": "Test x3000",
        "source": "test",
        "results": [
            {
                "name": "Test product",
                "url": "www.test.com",
                "image": "test.png",
                "price": 20.22,
            }
        ],
    }
    response = client.post("/product-results", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Received data successfully"


def test_get_product_result(client: TestClient, submit_product: ProductResult) -> None:
    response = client.get("/product-results", params={"search_text": "test-text"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert isinstance(data, list)
    product = data[0]
    assert product["name"] == "Test-product"
    assert product["price_history"][0]["price"] == 120.22
    assert product["source"] == "test-source"


def test_get_product_result_empty_list(client: TestClient, submit_product: ProductResult) -> None:
    response = client.get("/product-results", params={"search_text": "NOT FOUND"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    assert isinstance(data, list)
    assert data == []


def test_get_all_product_results(client: TestClient, submit_product: ProductResult) -> None:
    response = client.get("/product-results-all")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert isinstance(data, list)
    product_result = data[0]
    assert product_result["image"] == "test.png"
    assert product_result["name"] == "Test-product"
    assert product_result["price"] == 120.22
    assert product_result["source"] == "test-source"
    assert product_result["search_text"] == "test-text"
    assert product_result["url"] == "www.test.com"


def test_get_unique_search_text(client: TestClient, submit_product: ProductResult) -> None:
    response = client.get("/unique-search-texts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == ["test-text"]
