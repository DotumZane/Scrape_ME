import json
import logging
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class WebscraperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        json_data = None

        if user_input is not None:
            raw_json = user_input.get("config_json")
            try:
                json_data = json.loads(raw_json)
                # Basic validation
                if not json_data.get("target_url") or not json_data.get("css_selector"):
                    errors["base"] = "missing_fields"
                else:
                    return self.async_create_entry(
                        title=json_data.get("target_url", "Web Scraper"),
                        data={
                            "login_url": json_data.get("login_url", ""),
                            "target_url": json_data.get("target_url"),
                            "css_selector": json_data.get("css_selector"),
                            "cookies": json_data.get("cookies", []),
                        }
                    )
            except Exception as e:
                _LOGGER.exception("Failed to parse config JSON")
                errors["base"] = "invalid_json"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("config_json", default=""): str,
            }),
            errors=errors,
            description_placeholders={
                "help": "Paste the JSON exported from your browser extension here."
            }
        )
