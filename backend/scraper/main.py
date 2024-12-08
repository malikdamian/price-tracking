import asyncio

from backend.database import ProductResult
from backend.scraper.utils import load_auth, logger, post_results

from playwright.async_api import async_playwright, Playwright, Page

credential = load_auth()
auth = f"{credential["username"]}:{credential["password"]}"
SBR_WS_CDP = f"wss://{auth}@{credential["host"]}"

AMAZON = "https://amazon.pl"

URLS = {
    AMAZON: {
        "search_field_query": 'input[name="field-keywords"]',
        "search_button_query": 'input[value="Go"]',
        "product_selector": "div.s-card-container"
    }
}

async def search(metadata: dict[str, str], page: Page, search_text: str) -> Page:
    """
    Perform a search on the given page using the provided search text and metadata.

    This function automates the process of filling a search input field and clicking
    a search button on a webpage. It waits for the page to load completely before
    returning the page object
    
    :param metadata: A dictionary containing the CSS selectors for the serach field and search button.
        - "search_field_query": The CSS selector for the search input field.
        - "search_button_query": The CSS selector for the search button.
    :param page: The Playwright 'Page' object representing the current webpage.
    :param search_text: The text be entered into the serach input field

    :return: The Playwright 'Page' object after the search has been performed and the page has loaded.
    """
    logger.info(f"Searching for {search_text} on {page.url}")

    search_field_query = metadata.get("search_field_query")
    search_button_query = metadata.get("search_button_query")

    if not search_field_query or not search_button_query:
        raise Exception("Could not search")

    logger.info("Filling input field")
    search_box = await page.wait_for_selector(search_field_query)
    await search_box.type(search_text)
    logger.info("Pressing search button")
    button = await page.wait_for_selector(search_button_query)
    await button.click()

    await page.wait_for_load_state()
    return page


async def get_products(page: Page, search_text: str, selector: str, get_product) -> list[ProductResult]:
    logger.info("Retrieving products")

    product_divs = await page.query_selector_all(selector)
    valid_products = []
    words = search_text.split(" ")

    async with asyncio.TaskGroup() as tg:
        for div in product_divs:
            async def task(p_div):
                product = await get_product(p_div)

                if not product["price"] or not product["url"]:
                    return

                for word in words:
                    if not product.name or word.lower() not in product.name.lower():
                        break
                else:
                    valid_products.append(product)
            tg.create_task(task(div))

    return valid_products


async def run(pw: Playwright, url, metadata, search_text, response_route):
    logger.info('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        logger.info('Connected!')
        await page.goto(url, timeout=120000)
        logger.info("Loaded initial page.")
        search_page = await search(metadata, page, search_text)

        result = await get_products(search_page,  search_text, metadata["product_selector"])
        logger.info("Saving results")
        post_results(endpoint=response_route, product_result=result)

    finally:
        await browser.close()

async def main(url, search_text, response_route):
    metadata = URLS.get(url)

    if metadata is None:
        raise ValueError("Invalid URL")

    async with async_playwright() as playwright:
        await run(
            pw=playwright,
            url=url,
            metadata=metadata,
            search_text=search_text,
            response_route=response_route
        )
