from playwright.async_api import Page

from backend.scraper.utils import load_auth, logger

credential = load_auth()
auth = f"{credential["username"]}:{credential["password"]}"
browser_url = f"wss://{auth}@{credential["host"]}"


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
