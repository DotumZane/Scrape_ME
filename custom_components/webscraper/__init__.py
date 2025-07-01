import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "webscraper"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.debug("Setting up Webscraper integration (async_setup)")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up Webscraper config entry: %s", entry.as_dict())
    await hass.config_entries.async_forward_entry_setup(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading Webscraper config entry: %s", entry.as_dict())
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])

from .options_flow import WebscraperOptionsFlowHandler

async def async_get_options_flow(config_entry):
    return WebscraperOptionsFlowHandler(config_entry)
