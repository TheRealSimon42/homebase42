"""Binary sensor platform for Homebase42."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    NAME,
    CONF_BATTERY_CRITICAL_THRESHOLD,
    CONF_UNAVAILABLE_NOTIFICATION_DELAY,
    CONF_INCLUDE_HIDDEN_ENTITIES,
    DEFAULT_BATTERY_CRITICAL,
    DEFAULT_UNAVAILABLE_DELAY,
    DEFAULT_INCLUDE_HIDDEN_ENTITIES,
    ATTR_ENTITIES,
    ATTR_COUNT,
    ATTR_LAST_UPDATED,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Homebase42 binary sensors."""
    
    sensors = [
        Homebase42UnavailableSensor(hass, entry),
        Homebase42BatteryCriticalSensor(hass, entry),
    ]
    
    async_add_entities(sensors, True)


class Homebase42UnavailableSensor(BinarySensorEntity, RestoreEntity):
    """Binary sensor for unavailable entities."""

    _attr_has_entity_name = True
    _attr_translation_key = "unavailable_entities"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_unavailable_entities"
        self._unavailable_entities: list[str] = []
        self._attr_is_on = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=NAME,
            manufacturer="Simon42",
            model="Homebase42",
            sw_version="0.1.0",
        )

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        await super().async_added_to_hass()
        
        # Restore previous state
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_is_on = last_state.state == "on"
            if last_state.attributes.get(ATTR_ENTITIES):
                self._unavailable_entities = last_state.attributes[ATTR_ENTITIES]
        
        # Set up periodic update
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._async_update,
                SCAN_INTERVAL,
            )
        )
        
        # Initial update
        await self._async_update()

    @callback
    async def _async_update(self, now=None) -> None:
        """Update the sensor."""
        unavailable_entities = []
        delay_hours = self._entry.options.get(
            CONF_UNAVAILABLE_NOTIFICATION_DELAY, DEFAULT_UNAVAILABLE_DELAY
        )
        delay = timedelta(hours=delay_hours)
        include_hidden = self._entry.options.get(
            CONF_INCLUDE_HIDDEN_ENTITIES, DEFAULT_INCLUDE_HIDDEN_ENTITIES
        )
        now = dt_util.utcnow()
        
        # Get entity registry for checking hidden/disabled status
        entity_registry = er.async_get(self.hass)

        # Iterate through all entities
        for state in self.hass.states.async_all():
            # Skip entities from this integration
            if state.entity_id.startswith(f"binary_sensor.{DOMAIN}_") or \
               state.entity_id.startswith(f"sensor.{DOMAIN}_"):
                continue

            # Skip hidden entities if not configured to include them
            if not include_hidden:
                entity_entry = entity_registry.async_get(state.entity_id)
                if entity_entry:
                    # Check if entity is hidden or disabled in the registry
                    # hidden: boolean field set when entity visibility is set to false in UI
                    # hidden_by: string field (e.g., "user" or "integration")
                    # disabled_by: string field
                    if (entity_entry.hidden is True or 
                        entity_entry.hidden_by is not None or 
                        entity_entry.disabled_by is not None):
                        continue

            # Check if entity is unavailable
            if state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                # Check if it has been unavailable for long enough
                if state.last_changed and (now - state.last_changed) >= delay:
                    unavailable_entities.append(state.entity_id)
        
        self._unavailable_entities = unavailable_entities
        self._attr_is_on = len(unavailable_entities) > 0
        
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            ATTR_ENTITIES: self._unavailable_entities,
            ATTR_COUNT: len(self._unavailable_entities),
            ATTR_LAST_UPDATED: dt_util.utcnow().isoformat(),
        }


class Homebase42BatteryCriticalSensor(BinarySensorEntity, RestoreEntity):
    """Binary sensor for critical battery levels."""

    _attr_has_entity_name = True
    _attr_translation_key = "battery_critical"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:battery-alert"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_battery_critical"
        self._critical_batteries: list[str] = []
        self._attr_is_on = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=NAME,
            manufacturer="Simon42",
            model="Homebase42",
            sw_version="0.1.0",
        )

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        await super().async_added_to_hass()
        
        # Restore previous state
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_is_on = last_state.state == "on"
            if last_state.attributes.get(ATTR_ENTITIES):
                self._critical_batteries = last_state.attributes[ATTR_ENTITIES]
        
        # Set up periodic update
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._async_update,
                SCAN_INTERVAL,
            )
        )
        
        # Initial update
        await self._async_update()

    @callback
    async def _async_update(self, now=None) -> None:
        """Update the sensor."""
        critical_batteries = []
        threshold = self._entry.options.get(
            CONF_BATTERY_CRITICAL_THRESHOLD, DEFAULT_BATTERY_CRITICAL
        )
        include_hidden = self._entry.options.get(
            CONF_INCLUDE_HIDDEN_ENTITIES, DEFAULT_INCLUDE_HIDDEN_ENTITIES
        )
        
        # Get entity registry for checking hidden/disabled status
        entity_registry = er.async_get(self.hass)

        # Iterate through all sensor entities
        for state in self.hass.states.async_all("sensor"):
            # Skip hidden entities if not configured to include them
            if not include_hidden:
                entity_entry = entity_registry.async_get(state.entity_id)
                if entity_entry:
                    # Check if entity is hidden or disabled in the registry
                    # hidden: boolean field set when entity visibility is set to false in UI
                    # hidden_by: string field (e.g., "user" or "integration")
                    # disabled_by: string field
                    if (entity_entry.hidden is True or 
                        entity_entry.hidden_by is not None or 
                        entity_entry.disabled_by is not None):
                        continue

            # Check if it's a battery sensor
            if state.attributes.get("device_class") == "battery":
                try:
                    battery_level = float(state.state)
                    if battery_level <= threshold and state.state not in (
                        STATE_UNAVAILABLE,
                        STATE_UNKNOWN,
                    ):
                        critical_batteries.append(state.entity_id)
                except (ValueError, TypeError):
                    # Skip entities with non-numeric battery levels
                    continue
        
        self._critical_batteries = critical_batteries
        self._attr_is_on = len(critical_batteries) > 0
        
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            ATTR_ENTITIES: self._critical_batteries,
            ATTR_COUNT: len(self._critical_batteries),
            ATTR_LAST_UPDATED: dt_util.utcnow().isoformat(),
        }
