"""The Homebase42 integration."""
from __future__ import annotations

import logging
from pathlib import Path
import shutil
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

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


async def _async_copy_blueprints(hass: HomeAssistant) -> None:
    """Copy blueprints to the blueprints folder."""
    # Source: integration blueprints folder
    source_dir = Path(__file__).parent / "blueprints"
    
    # Destination: HA config/blueprints/automation/homebase42/
    dest_dir = Path(hass.config.path("blueprints", "automation", "homebase42"))
    
    if not source_dir.exists():
        _LOGGER.warning("Blueprints folder not found in integration")
        return
    
    try:
        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all blueprint files
        for blueprint_file in source_dir.glob("*.yaml"):
            dest_file = dest_dir / blueprint_file.name
            
            # Only copy if file doesn't exist or is different
            if not dest_file.exists() or dest_file.read_text() != blueprint_file.read_text():
                shutil.copy2(blueprint_file, dest_file)
                _LOGGER.info("Copied blueprint: %s", blueprint_file.name)
            else:
                _LOGGER.debug("Blueprint already up to date: %s", blueprint_file.name)
                
    except Exception as err:
        _LOGGER.error("Failed to copy blueprints: %s", err)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homebase42 from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Copy blueprints to user's blueprint folder
    await _async_copy_blueprints(hass)
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


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
