import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import timedelta

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .webscraper_api import WebScraperAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    _LOGGER.debug("Setting up sensor entity for Webscraper: %s", entry.as_dict())
    api = WebScraperAPI(entry.data)
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_coordinator",
        update_method=api.async_get_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([WebScraperSensor(coordinator, entry.data)], True)

class WebScraperSensor(Entity):
    def __init__(self, coordinator, config):
        self.coordinator = coordinator
        self._attr_name = config["name"]
        self._attr_unique_id = f"webscraper_{config['name'].lower().replace(' ','_')}"
        self._attr_extra_state_attributes = {
            "target_url": config["target_url"],
            "css_selector": config["css_selector"]
        }
        _LOGGER.debug("Webscraper sensor initialized with config: %s", config)

    @property
    def state(self):
        _LOGGER.debug("Getting sensor state: %s", self.coordinator.data)
        return self.coordinator.data

    async def async_update(self):
        _LOGGER.debug("Manual update triggered for Webscraper Sensor")
        await self.coordinator.async_request_refresh()
