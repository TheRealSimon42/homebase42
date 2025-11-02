"""Services for Homebase42."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import area_registry as ar, device_registry as dr, entity_registry as er
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DOMAIN,
    CONF_EXPORT_STATES_ENABLED,
    CONF_EXPORT_STATES_PATH,
    CONF_EXPORT_STATES_INTERVAL,
    DEFAULT_EXPORT_STATES_ENABLED,
    DEFAULT_EXPORT_STATES_PATH,
    DEFAULT_EXPORT_STATES_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

SERVICE_EXPORT_STATES = "export_states"
EXPORT_STARTUP_DELAY = timedelta(minutes=5)


async def async_setup_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up services for Homebase42."""
    
    # Get configuration options
    options = entry.options
    export_enabled = options.get(CONF_EXPORT_STATES_ENABLED, DEFAULT_EXPORT_STATES_ENABLED)
    export_path = options.get(CONF_EXPORT_STATES_PATH, DEFAULT_EXPORT_STATES_PATH)
    export_interval_minutes = options.get(CONF_EXPORT_STATES_INTERVAL, DEFAULT_EXPORT_STATES_INTERVAL)
    
    async def export_states_internal(
        output_path: str = "homebase42_state_export.json",
        include_attributes: bool = True,
        include_context: bool = True,
    ) -> None:
        """Internal function to export states."""
        _LOGGER.debug("Starting automatic state export to %s", output_path)
        
        try:
            # Get registries for additional context
            entity_reg = er.async_get(hass)
            area_reg = ar.async_get(hass)
            device_reg = dr.async_get(hass)
            
            # Build export data
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "home_assistant_version": hass.config.as_dict().get("version", "unknown"),
                "total_entities": 0,
                "states": [],
            }
            
            # Add summary by domain and area
            summary = {
                "by_domain": {},
                "by_area": {},
            }
            
            # Collect all states
            states_list = []
            for state in hass.states.async_all():
                entity_data = {
                    "entity_id": state.entity_id,
                    "state": state.state,
                    "domain": state.domain,
                }
                
                # Add basic attributes
                attributes = state.attributes or {}
                entity_data["friendly_name"] = attributes.get("friendly_name", "")
                entity_data["device_class"] = attributes.get("device_class", "")
                entity_data["unit"] = attributes.get("unit_of_measurement", "")
                entity_data["supported_features"] = attributes.get("supported_features", 0)
                
                # Get area from entity registry
                area_name = "None"
                if entity_entry := entity_reg.async_get(state.entity_id):
                    # Try to get area from entity first
                    if entity_entry.area_id:
                        if area := area_reg.async_get_area(entity_entry.area_id):
                            area_name = area.name
                    # If no area on entity, try device
                    elif entity_entry.device_id:
                        if device := device_reg.async_get(entity_entry.device_id):
                            if device.area_id:
                                if area := area_reg.async_get_area(device.area_id):
                                    area_name = area.name
                    
                    # Add entity registry info if requested
                    if include_context:
                        entity_data["entity_category"] = entity_entry.entity_category
                        entity_data["disabled"] = entity_entry.disabled
                        entity_data["hidden"] = entity_entry.hidden_by is not None
                        entity_data["platform"] = entity_entry.platform
                        entity_data["original_name"] = entity_entry.original_name
                
                entity_data["area"] = area_name
                
                # Add timestamps if requested
                if include_context:
                    entity_data["last_changed"] = state.last_changed.isoformat()
                    entity_data["last_updated"] = state.last_updated.isoformat()
                
                # Add all attributes if requested
                if include_attributes:
                    # Filter out large attributes and internal ones
                    filtered_attrs = {
                        k: v for k, v in attributes.items()
                        if k not in ["entity_picture", "friendly_name", "icon", "device_class", 
                                    "unit_of_measurement", "supported_features"]
                        and not isinstance(v, (bytes, bytearray))
                        and k != "attribution"
                    }
                    if filtered_attrs:
                        entity_data["attributes"] = filtered_attrs
                
                states_list.append(entity_data)
                
                # Update summary
                domain = state.domain
                summary["by_domain"][domain] = summary["by_domain"].get(domain, 0) + 1
                summary["by_area"][area_name] = summary["by_area"].get(area_name, 0) + 1
            
            # Sort by entity_id for consistent output
            states_list.sort(key=lambda x: x["entity_id"])
            
            export_data["states"] = states_list
            export_data["total_entities"] = len(states_list)
            export_data["summary"] = summary
            
            # Determine output file path
            if output_path.startswith("/"):
                # Absolute path
                file_path = Path(output_path)
            else:
                # Relative to config directory
                file_path = Path(hass.config.path(output_path))
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Add .json extension if not present
            if file_path.suffix != ".json":
                file_path = file_path.with_suffix(".json")
            
            # Write to file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            _LOGGER.info(
                "Successfully exported %d entities to %s",
                len(states_list),
                file_path,
            )
            
            # Fire event for automation triggers
            hass.bus.async_fire(
                f"{DOMAIN}_state_export_complete",
                {
                    "file_path": str(file_path),
                    "entity_count": len(states_list),
                    "timestamp": export_data["export_timestamp"],
                },
            )
            
        except Exception as err:
            _LOGGER.error("Failed to export states: %s", err, exc_info=True)

    async def handle_export_states(call: ServiceCall) -> None:
        """Handle the export_states service call."""
        # Get parameters from service call
        include_attributes = call.data.get("include_attributes", True)
        include_context = call.data.get("include_context", True)
        output_path = call.data.get("output_path", "homebase42_state_export.json")
        
        _LOGGER.info("Manual state export triggered to %s", output_path)
        
        await export_states_internal(output_path, include_attributes, include_context)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_EXPORT_STATES,
        handle_export_states,
        schema=None,  # We'll add validation in services.yaml
    )

    # Set up automatic export if enabled
    if export_enabled:
        # Automatic export timer callback
        @callback
        async def _handle_automatic_export(now=None) -> None:
            """Handle automatic state export."""
            await export_states_internal(export_path)
        
        # Schedule initial export after startup delay
        async def _schedule_initial_export(event) -> None:
            """Schedule the initial export after startup."""
            _LOGGER.info("Scheduling initial state export in %s to %s", EXPORT_STARTUP_DELAY, export_path)
            hass.async_call_later(
                EXPORT_STARTUP_DELAY.total_seconds(),
                _handle_automatic_export,
            )
        
        # Listen for HA start event
        hass.bus.async_listen_once("homeassistant_started", _schedule_initial_export)
        
        # Set up periodic export timer
        export_interval = timedelta(minutes=export_interval_minutes)
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN]["export_timer_remove"] = async_track_time_interval(
            hass,
            _handle_automatic_export,
            export_interval,
        )

        _LOGGER.info(
            "Homebase42 services registered (automatic export every %d minutes to %s)",
            export_interval_minutes,
            export_path,
        )
    else:
        _LOGGER.info("Homebase42 services registered (automatic export disabled)")


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Homebase42 services."""
    hass.services.async_remove(DOMAIN, SERVICE_EXPORT_STATES)
    
    # Cancel automatic export timer if it exists
    if DOMAIN in hass.data and "export_timer_remove" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["export_timer_remove"]()
        _LOGGER.debug("Automatic export timer cancelled")
    
    _LOGGER.info("Homebase42 services unloaded")
