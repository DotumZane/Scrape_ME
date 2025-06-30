import aiohttp
from bs4 import BeautifulSoup

class WebScraperAPI:
    def __init__(self, config):
        self._login_url = config["login_url"]
        self._username = config["username"]
        self._password = config["password"]
        self._target_url = config["target_url"]
        self._css_selector = config["css_selector"]
        self._session = None

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def async_get_data(self):
        await self._ensure_session()
        # 1. Login
        login_payload = {"username": self._username, "password": self._password}
        async with self._session.post(self._login_url, data=login_payload) as resp:
            if resp.status != 200:
                return "Login failed"
        # 2. Scrape
        async with self._session.get(self._target_url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            element = soup.select_one(self._css_selector)
            return element.text.strip() if element else "No element found"