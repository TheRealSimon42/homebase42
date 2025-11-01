"""Config flow for Homebase42 integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    NAME,
    CONF_BATTERY_CRITICAL_THRESHOLD,
    CONF_BATTERY_LOW_THRESHOLD,
    CONF_UNAVAILABLE_NOTIFICATION_DELAY,
    CONF_INCLUDE_HIDDEN_ENTITIES,
    DEFAULT_BATTERY_CRITICAL,
    DEFAULT_BATTERY_LOW,
    DEFAULT_UNAVAILABLE_DELAY,
    DEFAULT_INCLUDE_HIDDEN_ENTITIES,
)

_LOGGER = logging.getLogger(__name__)


class Homebase42ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Homebase42."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Only allow a single instance
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title=NAME,
                data={},
                options=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_BATTERY_CRITICAL_THRESHOLD,
                    default=DEFAULT_BATTERY_CRITICAL,
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
                vol.Optional(
                    CONF_BATTERY_LOW_THRESHOLD,
                    default=DEFAULT_BATTERY_LOW,
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
                vol.Optional(
                    CONF_UNAVAILABLE_NOTIFICATION_DELAY,
                    default=DEFAULT_UNAVAILABLE_DELAY,
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
                vol.Optional(
                    CONF_INCLUDE_HIDDEN_ENTITIES,
                    default=DEFAULT_INCLUDE_HIDDEN_ENTITIES,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> Homebase42OptionsFlow:
        """Get the options flow for this handler."""
        return Homebase42OptionsFlow(config_entry)


class Homebase42OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Homebase42."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_BATTERY_CRITICAL_THRESHOLD,
                    default=options.get(
                        CONF_BATTERY_CRITICAL_THRESHOLD, DEFAULT_BATTERY_CRITICAL
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
                vol.Optional(
                    CONF_BATTERY_LOW_THRESHOLD,
                    default=options.get(CONF_BATTERY_LOW_THRESHOLD, DEFAULT_BATTERY_LOW),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
                vol.Optional(
                    CONF_UNAVAILABLE_NOTIFICATION_DELAY,
                    default=options.get(
                        CONF_UNAVAILABLE_NOTIFICATION_DELAY, DEFAULT_UNAVAILABLE_DELAY
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
                vol.Optional(
                    CONF_INCLUDE_HIDDEN_ENTITIES,
                    default=options.get(
                        CONF_INCLUDE_HIDDEN_ENTITIES, DEFAULT_INCLUDE_HIDDEN_ENTITIES
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
