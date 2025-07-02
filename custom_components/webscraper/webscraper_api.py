import logging
import aiohttp
from bs4 import BeautifulSoup
import re

_LOGGER = logging.getLogger(__name__)

class WebScraperAPI:
    def __init__(self, config):
        self._login_url = config["login_url"]
        self._username = config["username"]
        self._password = config["password"]
        self._target_url = config["target_url"]
        self._css_selector = config["css_selector"]
        self._session = None
        _LOGGER.debug("WebScraperAPI initialized with config: %s", config)

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            _LOGGER.debug("Creating new aiohttp ClientSession")
            self._session = aiohttp.ClientSession()

    async def test_login(self):
        await self._ensure_session()
        login_payload = {"username": self._username, "password": self._password}
        try:
            async with self._session.post(self._login_url, data=login_payload) as resp:
                _LOGGER.debug("Test login response status: %s", resp.status)
                if resp.status != 200:
                    raise Exception(f"Login failed: {resp.status}")
        except Exception as e:
            _LOGGER.error("Exception during test login: %s", e)
            raise

    async def async_get_data(self):
        await self._ensure_session()
        # 1. Login
        login_payload = {"username": self._username, "password": self._password}
        _LOGGER.debug("Attempting login to %s with username %s", self._login_url, self._username)
        try:
            async with self._session.post(self._login_url, data=login_payload) as resp:
                _LOGGER.debug("Login response status: %s", resp.status)
                if resp.status != 200:
                    _LOGGER.error("Login failed to %s, status: %s", self._login_url, resp.status)
                    return "Login failed"
        except Exception as e:
            _LOGGER.error("Exception during login: %s", e)
            return f"Login exception: {e}"

        # 2. Scrape
        try:
            async with self._session.get(self._target_url) as resp:
                _LOGGER.debug("Scraping %s, status: %s", self._target_url, resp.status)
                html = await resp.text()
                # Optional: log a snippet of HTML for debugging
                _LOGGER.debug("Fetched HTML snippet: %s", html[:300])
                soup = BeautifulSoup(html, "html.parser")
                element = soup.select_one(self._css_selector)
                if element:
                    # Prefer value attribute if present, else use text
                    value = element.get('value', None)
                    if value is None:
                        value = element.text.strip()
                    else:
                        value = value.strip()
                    # Extract first number (including decimals)
                    match = re.search(r"(\d+(\.\d+)?)", value)
                    if match:
                        result = float(match.group(1))
                        _LOGGER.debug("Scrape result (number): %s", result)
                        return result
                    else:
                        _LOGGER.warning("Could not find a number in the element content: '%s'", value)
                        return "No number found"
                else:
                    _LOGGER.warning("No element found for selector: %s", self._css_selector)
                    return "No element found"
        except Exception as e:
            _LOGGER.error("Exception during scraping: %s", e)
            return f"Scraping exception: {e}"
