"""Binary sensor platform for Homebase42."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    CONF_BATTERY_CRITICAL_THRESHOLD,
    DEFAULT_BATTERY_CRITICAL,
    ATTR_ENTITIES,
    ATTR_COUNT,
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
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_unavailable_entities"
        self._attr_name = "Nicht verfügbare Entitäten"
        self._unavailable_entities: list[str] = []
        self._attr_is_on = False

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
        unavailable = []
        
        # Get all entities from the registry
        entity_registry = self.hass.helpers.entity_registry.async_get(self.hass)
        
        for entity_id, entity in entity_registry.entities.items():
            # Skip disabled entities
            if entity.disabled:
                continue
            
            # Skip config/diagnostic entities
            if entity.entity_category:
                continue
            
            # Check if entity is unavailable in states
            state = self.hass.states.get(entity_id)
            if state and state.state == "unavailable":
                unavailable.append(entity_id)
        
        self._unavailable_entities = unavailable
        self._attr_is_on = len(unavailable) > 0
        
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            ATTR_ENTITIES: self._unavailable_entities,
            ATTR_COUNT: len(self._unavailable_entities),
        }


class Homebase42BatteryCriticalSensor(BinarySensorEntity, RestoreEntity):
    """Binary sensor for critical battery levels."""

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.BATTERY
    _attr_icon = "mdi:battery-alert"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_battery_critical"
        self._attr_name = "Kritische Batteriestände"
        self._critical_batteries: list[str] = []
        self._attr_is_on = False

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
        critical = []
        threshold = self._entry.options.get(
            CONF_BATTERY_CRITICAL_THRESHOLD, DEFAULT_BATTERY_CRITICAL
        )
        
        # Get all battery entities
        entity_registry = self.hass.helpers.entity_registry.async_get(self.hass)
        
        for entity_id, entity in entity_registry.entities.items():
            # Skip disabled entities
            if entity.disabled:
                continue
            
            # Check for battery entities
            if not (
                entity.device_class == "battery"
                or entity.original_device_class == "battery"
                or "battery" in entity_id.lower()
            ):
                continue
            
            # Check battery level
            state = self.hass.states.get(entity_id)
            if state and state.state not in ("unavailable", "unknown"):
                try:
                    level = float(state.state)
                    if level <= threshold:
                        critical.append(entity_id)
                except (ValueError, TypeError):
                    continue
        
        self._critical_batteries = critical
        self._attr_is_on = len(critical) > 0
        
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            ATTR_ENTITIES: self._critical_batteries,
            ATTR_COUNT: len(self._critical_batteries),
        }
