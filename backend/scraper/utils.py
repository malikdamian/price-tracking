import json
import logging
import os.path

import requests

from backend.config import settings
from backend.database import ProductResult

logger = logging.getLogger(__name__)


def load_auth():
    path_file = os.path.join("scraper", "auth.json")

    with open(path_file, "r") as file:
        return json.load(file)


def post_results(endpoint: str, product_result: ProductResult) -> dict[str, str]:
    headers: dict[str, str] = {"Content-Type": "application/json"}

    host = settings.HOST
    port = settings.PORT
    url = f"http://{host}:{port}{endpoint}"

    logger.info(f"Sending request to {endpoint}")
    response = requests.post(url, headers=headers, json=product_result)
    response.raise_for_status()

    logger.info(f"Status code: {response.status_code}")
    return {"message": "Successfully posted results"}


def save_results(results):
    data = {"results": results}
    file = os.path.join("Scraper", "results.json")
    with open(file, "w") as f:
        json.dump(data, f)

