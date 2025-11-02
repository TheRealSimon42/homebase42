"""The Homebase42 integration."""
from __future__ import annotations

import logging
from pathlib import Path
import shutil
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir

from .const import (
    DOMAIN,
    BLUEPRINTS_CORE,
    BLUEPRINTS_OPTIONAL,
    OPTIONAL_BLUEPRINTS,
    TEMPLATES_OPTIONAL,
    OPTIONAL_TEMPLATES,
    CONF_WEATHER_ENTITY,
    DEFAULT_WEATHER_ENTITY,
    REPAIR_RESTART_REQUIRED,
)
from .services import async_setup_services, async_unload_services

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
    
    # Services will be registered when a config entry is set up
    # (we need the config entry for options)

    return True


def _copy_blueprints_sync(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Copy blueprints to the blueprints folder based on configuration (sync version).
    
    Returns True if blueprints were changed (added/removed/updated), False otherwise.
    """
    # Source: integration blueprints folder
    blueprints_dir = Path(__file__).parent / "blueprints"
    
    # Destination: HA config/blueprints/automation/homebase42/
    dest_dir = Path(hass.config.path("blueprints", "automation", "homebase42"))
    
    if not blueprints_dir.exists():
        _LOGGER.warning("Blueprints folder not found in integration")
        return False
    
    blueprints_changed = False
    
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
                    blueprints_changed = True
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
                            blueprints_changed = True
                        else:
                            _LOGGER.debug("Optional blueprint already up to date: %s", blueprint_filename)
                else:
                    # Blueprint is disabled -> remove it if it exists
                    if dest_file.exists():
                        dest_file.unlink()
                        _LOGGER.info("Removed disabled optional blueprint: %s", blueprint_filename)
                        blueprints_changed = True
                
    except Exception as err:
        _LOGGER.error("Failed to manage blueprints: %s", err)
        return False
    
    return blueprints_changed


async def _async_copy_blueprints(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Copy blueprints to the blueprints folder based on configuration.
    
    Returns True if blueprints were changed, False otherwise.
    """
    return await hass.async_add_executor_job(_copy_blueprints_sync, hass, entry)


def _copy_templates_sync(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Copy templates to the packages folder based on configuration (sync version).
    
    Returns True if templates were changed (added/removed/updated), False otherwise.
    """
    # Source: integration templates folder
    templates_dir = Path(__file__).parent / "templates"
    
    # Destination: HA config/packages/homebase42/
    dest_dir = Path(hass.config.path("packages", "homebase42"))
    
    if not templates_dir.exists():
        _LOGGER.debug("Templates folder not found in integration")
        return False
    
    templates_changed = False
    
    try:
        # Get options from config entry
        options = entry.options
        weather_entity = options.get(CONF_WEATHER_ENTITY, DEFAULT_WEATHER_ENTITY)
        
        # Handle OPTIONAL templates based on configuration
        optional_dir = templates_dir / TEMPLATES_OPTIONAL
        if optional_dir.exists():
            for template_filename, config_key in OPTIONAL_TEMPLATES.items():
                template_file = optional_dir / template_filename
                
                # Check if this optional template is enabled
                is_enabled = options.get(config_key, False)
                
                if is_enabled:
                    # Template is enabled -> copy it with weather entity replacement
                    if template_file.exists():
                        # Create destination directory if needed
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        dest_file = dest_dir / template_filename
                        
                        # Read template content and replace placeholder
                        content = template_file.read_text()
                        content = content.replace("WEATHER_ENTITY_PLACEHOLDER", weather_entity)
                        
                        # Write to destination if different
                        if not dest_file.exists() or dest_file.read_text() != content:
                            dest_file.write_text(content)
                            _LOGGER.info("Copied optional template: %s (using %s)", template_filename, weather_entity)
                            templates_changed = True
                        else:
                            _LOGGER.debug("Optional template already up to date: %s", template_filename)
                else:
                    # Template is disabled -> remove it if it exists
                    dest_file = dest_dir / template_filename
                    if dest_file.exists():
                        dest_file.unlink()
                        _LOGGER.info("Removed disabled optional template: %s", template_filename)
                        templates_changed = True
                        
                        # Remove directory if empty
                        if dest_dir.exists() and not any(dest_dir.iterdir()):
                            dest_dir.rmdir()
                            _LOGGER.debug("Removed empty packages/homebase42 directory")
                
    except Exception as err:
        _LOGGER.error("Failed to manage templates: %s", err)
        return False
    
    return templates_changed


async def _async_copy_templates(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Copy templates to the packages folder based on configuration.
    
    Returns True if templates were changed, False otherwise.
    """
    return await hass.async_add_executor_job(_copy_templates_sync, hass, entry)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homebase42 from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Copy blueprints to user's blueprint folder
    blueprints_changed = await _async_copy_blueprints(hass, entry)
    
    # Copy templates to user's packages folder
    templates_changed = await _async_copy_templates(hass, entry)
    
    # If blueprints or templates were changed, create a repair issue to notify user about restart
    if blueprints_changed or templates_changed:
        ir.async_create_issue(
            hass,
            DOMAIN,
            REPAIR_RESTART_REQUIRED,
            is_fixable=False,
            severity=ir.IssueSeverity.WARNING,
            translation_key="restart_required",
        )
    else:
        # Remove repair issue if it exists (everything is up to date)
        ir.async_delete_issue(hass, DOMAIN, REPAIR_RESTART_REQUIRED)
    
    # Register services (only once for the first config entry)
    if len([e for e in hass.config_entries.async_entries(DOMAIN)]) == 1:
        await async_setup_services(hass, entry)
    
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
        
        # Unload services if no more config entries
        if not hass.data[DOMAIN]:
            await async_unload_services(hass)
    
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
