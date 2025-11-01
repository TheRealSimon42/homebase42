"""The Homebase42 integration."""
from __future__ import annotations

import logging
from pathlib import Path
import shutil
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    BLUEPRINTS_CORE,
    BLUEPRINTS_OPTIONAL,
    OPTIONAL_BLUEPRINTS,
)

if TYPE_CHECKING:
    from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Homebase42 component."""
    hass.data.setdefault(DOMAIN, {})

    return True


async def _async_copy_blueprints(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Copy blueprints to the blueprints folder based on configuration."""
    # Source: integration blueprints folder
    blueprints_dir = Path(__file__).parent / "blueprints"
    
    # Destination: HA config/blueprints/automation/homebase42/
    dest_dir = Path(hass.config.path("blueprints", "automation", "homebase42"))
    
    if not blueprints_dir.exists():
        _LOGGER.warning("Blueprints folder not found in integration")
        return
    
    try:
        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Get options from config entry
        options = entry.options
        
        # 1. Copy all CORE blueprints (always installed)
        core_dir = blueprints_dir / BLUEPRINTS_CORE
        if core_dir.exists():
            for blueprint_file in core_dir.glob("*.yaml"):
                dest_file = dest_dir / blueprint_file.name
                
                # Only copy if file doesn't exist or is different
                if not dest_file.exists() or dest_file.read_text() != blueprint_file.read_text():
                    shutil.copy2(blueprint_file, dest_file)
                    _LOGGER.info("Copied core blueprint: %s", blueprint_file.name)
                else:
                    _LOGGER.debug("Core blueprint already up to date: %s", blueprint_file.name)
        
        # 2. Handle OPTIONAL blueprints based on configuration
        optional_dir = blueprints_dir / BLUEPRINTS_OPTIONAL
        if optional_dir.exists():
            for blueprint_filename, config_key in OPTIONAL_BLUEPRINTS.items():
                blueprint_file = optional_dir / blueprint_filename
                dest_file = dest_dir / blueprint_filename
                
                # Check if this optional blueprint is enabled
                is_enabled = options.get(config_key, False)
                
                if is_enabled:
                    # Blueprint is enabled -> copy it
                    if blueprint_file.exists():
                        if not dest_file.exists() or dest_file.read_text() != blueprint_file.read_text():
                            shutil.copy2(blueprint_file, dest_file)
                            _LOGGER.info("Copied optional blueprint: %s", blueprint_filename)
                        else:
                            _LOGGER.debug("Optional blueprint already up to date: %s", blueprint_filename)
                else:
                    # Blueprint is disabled -> remove it if it exists
                    if dest_file.exists():
                        dest_file.unlink()
                        _LOGGER.info("Removed disabled optional blueprint: %s", blueprint_filename)
                
    except Exception as err:
        _LOGGER.error("Failed to manage blueprints: %s", err)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homebase42 from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Copy blueprints to user's blueprint folder
    await _async_copy_blueprints(hass, entry)
    
    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry.
    
    Note: Blueprints are NOT automatically deleted to preserve any automations
    that users may have created based on them. If you want to remove the blueprints,
    manually delete the folder: config/blueprints/automation/homebase42/
    """
    _LOGGER.info(
        "Integration removed. Blueprints are kept in blueprints/automation/homebase42/. "
        "Delete manually if no longer needed."
    )
