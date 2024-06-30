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
