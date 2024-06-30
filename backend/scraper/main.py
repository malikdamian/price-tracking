from playwright.async_api import Page

from backend.scraper.utils import load_auth, logger

credential = load_auth()
auth = f"{credential["username"]}:{credential["password"]}"
browser_url = f"wss://{auth}@{credential["host"]}"


async def search(metadata: dict[str, str], page: Page, search_text: str) -> Page:
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
