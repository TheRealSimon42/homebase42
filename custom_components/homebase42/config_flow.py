"""Config flow for Homebase42 integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    NAME,
    CONF_BATTERY_CRITICAL_THRESHOLD,
    CONF_BATTERY_LOW_THRESHOLD,
    CONF_UNAVAILABLE_NOTIFICATION_DELAY,
    CONF_INCLUDE_HIDDEN_ENTITIES,
    CONF_WEATHER_ENTITY,
    CONF_CONFIGURE_BLUEPRINTS,
    CONF_CONFIGURE_WEATHER,
    CONF_BLUEPRINT_FRIENT_KEYPAD,
    CONF_TEMPLATE_WEATHER,
    DEFAULT_BATTERY_CRITICAL,
    DEFAULT_BATTERY_LOW,
    DEFAULT_UNAVAILABLE_DELAY,
    DEFAULT_INCLUDE_HIDDEN_ENTITIES,
    DEFAULT_WEATHER_ENTITY,
    DEFAULT_CONFIGURE_BLUEPRINTS,
    DEFAULT_CONFIGURE_WEATHER,
    DEFAULT_BLUEPRINT_FRIENT_KEYPAD,
    DEFAULT_TEMPLATE_WEATHER,
)

_LOGGER = logging.getLogger(__name__)


class Homebase42ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Homebase42."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._user_input: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Only allow a single instance
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            self._user_input.update(user_input)
            
            # Check if we need to show blueprints step
            if user_input.get(CONF_CONFIGURE_BLUEPRINTS, False):
                return await self.async_step_blueprints()
            else:
                # User didn't select blueprints, set all blueprint options to False
                self._user_input[CONF_BLUEPRINT_FRIENT_KEYPAD] = False
            
            # Check if we need to show weather step
            if user_input.get(CONF_CONFIGURE_WEATHER, False):
                return await self.async_step_weather()
            else:
                # User didn't select weather configuration, set to False
                self._user_input[CONF_TEMPLATE_WEATHER] = False
            
            # No additional steps needed, create entry
            return self.async_create_entry(
                title=NAME,
                data={},
                options=self._user_input,
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
                vol.Optional(
                    CONF_CONFIGURE_BLUEPRINTS,
                    default=DEFAULT_CONFIGURE_BLUEPRINTS,
                ): bool,
                vol.Optional(
                    CONF_CONFIGURE_WEATHER,
                    default=DEFAULT_CONFIGURE_WEATHER,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )

    async def async_step_blueprints(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the blueprints selection step."""
        if user_input is not None:
            self._user_input.update(user_input)
            
            # Check if we need to show weather step
            if self._user_input.get(CONF_CONFIGURE_WEATHER, False):
                return await self.async_step_weather()
            else:
                # User didn't select weather configuration, set to False
                self._user_input[CONF_TEMPLATE_WEATHER] = False
            
            # No more steps, create entry
            return self.async_create_entry(
                title=NAME,
                data={},
                options=self._user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_BLUEPRINT_FRIENT_KEYPAD,
                    default=DEFAULT_BLUEPRINT_FRIENT_KEYPAD,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="blueprints",
            data_schema=data_schema,
        )

    async def async_step_weather(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the weather configuration step."""
        if user_input is not None:
            self._user_input.update(user_input)
            # Set template_weather to True since user went through this step
            self._user_input[CONF_TEMPLATE_WEATHER] = True
            
            return self.async_create_entry(
                title=NAME,
                data={},
                options=self._user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_WEATHER_ENTITY,
                    default=DEFAULT_WEATHER_ENTITY,
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="weather")
                ),
            }
        )

        return self.async_show_form(
            step_id="weather",
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
        self._user_input: dict[str, Any] = {}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            self._user_input.update(user_input)
            
            # Check if we need to show blueprints step
            if user_input.get(CONF_CONFIGURE_BLUEPRINTS, False):
                return await self.async_step_blueprints_options()
            else:
                # User didn't select blueprints, set all blueprint options to False
                self._user_input[CONF_BLUEPRINT_FRIENT_KEYPAD] = False
            
            # Check if we need to show weather step
            if user_input.get(CONF_CONFIGURE_WEATHER, False):
                return await self.async_step_weather_options()
            else:
                # User didn't select weather configuration, set to False
                self._user_input[CONF_TEMPLATE_WEATHER] = False
            
            # No additional steps needed, create entry
            return self.async_create_entry(title="", data=self._user_input)

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
                vol.Optional(
                    CONF_CONFIGURE_BLUEPRINTS,
                    default=options.get(
                        CONF_CONFIGURE_BLUEPRINTS, DEFAULT_CONFIGURE_BLUEPRINTS
                    ),
                ): bool,
                vol.Optional(
                    CONF_CONFIGURE_WEATHER,
                    default=options.get(
                        CONF_CONFIGURE_WEATHER, DEFAULT_CONFIGURE_WEATHER
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )

    async def async_step_blueprints_options(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the blueprints selection step in options."""
        if user_input is not None:
            self._user_input.update(user_input)
            
            # Check if we need to show weather step
            if self._user_input.get(CONF_CONFIGURE_WEATHER, False):
                return await self.async_step_weather_options()
            else:
                # User didn't select weather configuration, set to False
                self._user_input[CONF_TEMPLATE_WEATHER] = False
            
            # No more steps, create entry
            return self.async_create_entry(title="", data=self._user_input)

        options = self.config_entry.options

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_BLUEPRINT_FRIENT_KEYPAD,
                    default=options.get(
                        CONF_BLUEPRINT_FRIENT_KEYPAD, DEFAULT_BLUEPRINT_FRIENT_KEYPAD
                    ),
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="blueprints_options",
            data_schema=data_schema,
        )

    async def async_step_weather_options(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the weather configuration step in options."""
        if user_input is not None:
            self._user_input.update(user_input)
            # Set template_weather to True since user went through this step
            self._user_input[CONF_TEMPLATE_WEATHER] = True
            
            return self.async_create_entry(title="", data=self._user_input)

        options = self.config_entry.options

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_WEATHER_ENTITY,
                    default=options.get(CONF_WEATHER_ENTITY, DEFAULT_WEATHER_ENTITY),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="weather")
                ),
            }
        )

        return self.async_show_form(
            step_id="weather_options",
            data_schema=data_schema,
        )
