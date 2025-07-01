import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.exceptions import ConfigEntryNotReady

from .webscraper_api import WebScraperAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "webscraper"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.debug("Setting up Webscraper integration (async_setup)")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up Webscraper config entry: %s", entry.as_dict())
    # Try initial login/check here (before platform setup)
    data = {**entry.data, **entry.options}
    api = WebScraperAPI(data)
    try:
        await api.test_login()
    except Exception as e:
        _LOGGER.error("Webscraper login test failed: %s", e)
        raise ConfigEntryNotReady(f"Webscraper login failed: {e}")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading Webscraper config entry: %s", entry.as_dict())
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
