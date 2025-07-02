import logging
import aiohttp
from bs4 import BeautifulSoup

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
                soup = BeautifulSoup(html, "html.parser")
                element = soup.select_one(self._css_selector)
if element:
    # If it's an input or similar, get 'value', else get text
    value = element.get('value', None)
    if value is not None:
        result = value.strip()
    else:
        result = element.text.strip()
    _LOGGER.debug("Scrape result: %s", result)
    return result
else:
    _LOGGER.warning("No element found for selector: %s", self._css_selector)
    return "No element found"
                else:
                    _LOGGER.warning("No element found for selector: %s", self._css_selector)
                    return "No element found"
        except Exception as e:
            _LOGGER.error("Exception during scraping: %s", e)
            return f"Scraping exception: {e}"
