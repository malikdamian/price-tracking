from backend.scraper.utils import load_auth

credential = load_auth()
auth = f"{credential["username"]}:{credential["password"]}"
browser_url = f"wss://{auth}@{credential["host"]}"
