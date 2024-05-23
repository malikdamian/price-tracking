def test_submit_product_result(client):
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
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["message"] == "Received data successfully"
