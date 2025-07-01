import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

class WebscraperOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        options = self.config_entry.options

        def get_value(key):
            return options.get(key, data.get(key, ""))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("name", default=get_value("name")): str,
                vol.Required("login_url", default=get_value("login_url")): str,
                vol.Required("username", default=get_value("username")): str,
                vol.Required("password", default=get_value("password")): str,
                vol.Required("target_url", default=get_value("target_url")): str,
                vol.Required("css_selector", default=get_value("css_selector")): str,
            }),
        )
