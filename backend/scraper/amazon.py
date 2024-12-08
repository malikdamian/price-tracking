from asyncio import gather

from playwright.async_api import ElementHandle

from backend.schemas import Result


async def get_product(product_div: ElementHandle) -> Result:
    """
    Extract product details from a given product division element.

    :param product_div: The product division element handle.
    :return: Result object
    """
    image_element_future = product_div.query_selector("img.s-image")
    name_element_future = product_div.query_selector("h2 a span")
    price_element_future = product_div.query_selector("span.a-offscreen")
    url_element_future = product_div.query_selector(
        "a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
    )

    image_element, name_element, price_element, url_element = await gather(
        image_element_future,
        name_element_future,
        price_element_future,
        url_element_future,
    )

    image_url = await image_element.get_attribute("src") if image_element else None
    product_name = await name_element.inner_text() if name_element else None
    product_price = await get_price(price_element)
    product_url = await process_url(url_element)

    return Result(name=product_name, url=product_url, image=image_url, price=product_price)


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
