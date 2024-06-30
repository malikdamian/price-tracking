from asyncio import gather

from playwright.async_api import ElementHandle

from backend.schemas import Result


async def get_price(price_element: ElementHandle | None) -> float | None:
    """
    Extract and process the product price from the price element.

    :param price_element: The price element handle.

    :returns: The product price as a float, or None if not available.
    """
    if not price_element:
        return None

    price_text = await price_element.inner_text()
    price_text = price_text.replace("zł", "").replace(",", ".").strip()

    try:
        return float(price_text)
    except ValueError:
        raise ValueError("Invalid price text")


async def process_url(url_element: ElementHandle | None) -> str | None:
    """
    Process and clean the product URL from the URL element.

    :param url_element: The URL element handle.
    returns: The cleaned product URL, or None if not available.
    """
    if not url_element:
        return None

    if url := await url_element.get_attribute("href"):
        return "/".join(url.split("/")[:4])
