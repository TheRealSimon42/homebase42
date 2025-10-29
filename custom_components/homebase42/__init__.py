"""The Homebase42 integration."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.loader import async_get_integration

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
    
    # Register the dashboard strategy resources
    # This makes the simon42-strategy files available at /hacsfiles/homebase42/
    integration = await async_get_integration(hass, DOMAIN)
    
    # Register static path for strategy files
    hass.http.register_static_path(
        f"/hacsfiles/{DOMAIN}",
        str(integration.file_path / "www"),
        cache_headers=False,
    )
    
    _LOGGER.info("Homebase42 dashboard strategy registered at /hacsfiles/%s/", DOMAIN)
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homebase42 from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
