"""Sensor platform for Homebase42."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    CONF_BATTERY_CRITICAL_THRESHOLD,
    CONF_BATTERY_LOW_THRESHOLD,
    DEFAULT_BATTERY_CRITICAL,
    DEFAULT_BATTERY_LOW,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Homebase42 sensors."""
    
    sensors = [
        Homebase42UnavailableCountSensor(hass, entry),
        Homebase42BatteryLowCountSensor(hass, entry),
    ]
    
    async_add_entities(sensors, True)


class Homebase42UnavailableCountSensor(SensorEntity, RestoreEntity):
    """Sensor for counting unavailable entities."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:counter"
    _attr_native_unit_of_measurement = "entities"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_unavailable_count"
        self._attr_name = "Anzahl nicht verfügbarer Entitäten"
        self._attr_native_value = 0

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        await super().async_added_to_hass()
        
        # Restore previous state
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._attr_native_value = int(last_state.state)
            except (ValueError, TypeError):
                self._attr_native_value = 0
        
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
        count = 0
        
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
                count += 1
        
        self._attr_native_value = count
        self.async_write_ha_state()


class Homebase42BatteryLowCountSensor(SensorEntity, RestoreEntity):
    """Sensor for counting low battery entities."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:battery-low"
    _attr_native_unit_of_measurement = "entities"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_battery_low_count"
        self._attr_name = "Anzahl Batterien mit niedrigem Stand"
        self._attr_native_value = 0

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        await super().async_added_to_hass()
        
        # Restore previous state
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._attr_native_value = int(last_state.state)
            except (ValueError, TypeError):
                self._attr_native_value = 0
        
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
        count = 0
        critical_threshold = self._entry.options.get(
            CONF_BATTERY_CRITICAL_THRESHOLD, DEFAULT_BATTERY_CRITICAL
        )
        low_threshold = self._entry.options.get(
            CONF_BATTERY_LOW_THRESHOLD, DEFAULT_BATTERY_LOW
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
            
            # Check battery level (low but not critical)
            state = self.hass.states.get(entity_id)
            if state and state.state not in ("unavailable", "unknown"):
                try:
                    level = float(state.state)
                    if critical_threshold < level <= low_threshold:
                        count += 1
                except (ValueError, TypeError):
                    continue
        
        self._attr_native_value = count
        self.async_write_ha_state()
