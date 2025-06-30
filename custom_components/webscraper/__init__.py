from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import service
from .webscraper_api import WebScraperAPI

import logging

DOMAIN = "scrape_me"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # Register debug service
    async def handle_debug_service(call: ServiceCall):
        api = WebScraperAPI(entry.data)
        try:
            result = await api.async_get_data()
            _LOGGER.info("Scrape ME debug result: %s", result)
            hass.async_create_task(
                hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "title": "Scrape ME Debug Result",
                        "message": f"Result: {result}"
                    }
                )
            )
        except Exception as e:
            _LOGGER.error("Scrape ME debug error: %s", str(e))
            hass.async_create_task(
                hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "title": "Scrape ME Debug Error",
                        "message": str(e)
                    }
                )
            )

    hass.services.async_register(DOMAIN, "debug", handle_debug_service)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "webscraper"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
