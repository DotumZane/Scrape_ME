from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class WebScraperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Could add validation here (attempt login/scrape)
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("login_url"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("target_url"): str,
                vol.Required("css_selector"): str,
            }),
            errors=errors,
        )