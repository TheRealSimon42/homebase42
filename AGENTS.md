# Agent Guide for Homebase42

## Project Overview
This is a Home Assistant custom integration for monitoring entities and battery levels. It follows Home Assistant's integration architecture standards.

## Build/Test Commands
No formal test suite currently exists. Manual testing requires:
- Install integration in a Home Assistant instance (copy `custom_components/homebase42` to HA config)
- Restart Home Assistant
- Add integration via UI: Settings → Devices & Services → Add Integration → Homebase42

## Code Style Guidelines

### Imports
- Use `from __future__ import annotations` at top of every Python file
- Group imports: stdlib, third-party (homeassistant), local (.const, etc.)
- Use TYPE_CHECKING for type-only imports to avoid circular dependencies
- Example from `__init__.py:1-14`

### Types & Annotations
- Always add type hints to function parameters and return types
- Use Home Assistant typing helpers: `from homeassistant.helpers.typing import ConfigType`
- Use modern type syntax with `|` for Optional (e.g., `dict[str, Any] | None`)

### Naming Conventions
- Classes: PascalCase (e.g., `Homebase42UnavailableSensor`)
- Functions/methods: snake_case (e.g., `async_setup_entry`)
- Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_BATTERY_CRITICAL`)
- Private attributes: prefix with `_` (e.g., `self._unavailable_entities`)

### Error Handling
- Use try/except for parsing user data (e.g., `float(state.state)`)
- Log exceptions with `_LOGGER.error()` or `_LOGGER.warning()`
- Gracefully skip invalid entities with `continue` in loops

### Home Assistant Specific
- Use `async/await` for all integration entry points
- Entities must have `unique_id` for persistence
- Use `@callback` for update methods
- Implement `RestoreEntity` for state persistence across restarts
- Use `hass.states.async_all()` for efficient state iteration
- Device info should include: identifiers, name, manufacturer, model, sw_version
- Translation keys in `_attr_translation_key` map to `translations/en.json`

### File Structure
- `__init__.py`: Integration setup/teardown
- `const.py`: All constants and configuration keys
- `config_flow.py`: UI configuration flow
- `sensor.py`/`binary_sensor.py`: Entity platforms
- `manifest.json`: Integration metadata
- `blueprints/core/`: Core blueprints (always installed)
- `blueprints/optional/`: Optional blueprints (user-selectable)

## Blueprint Management

### Blueprint Directory Structure
```
blueprints/
├── core/                              # Always installed
│   ├── s42_unavailable_notification.yaml
│   └── s42_persistent_notification_to_mobile.yaml
└── optional/                          # Only installed when enabled by user
    └── s42_frient_keypad.yaml
```

### How Blueprints Work
1. **Core blueprints** are automatically copied to `config/blueprints/automation/homebase42/` on setup
2. **Optional blueprints** are only copied when user enables them in the config flow
3. Blueprints are managed via the Options Flow (Devices & Services → Homebase42 → Configure)
4. When a user disables an optional blueprint, the file is automatically deleted
5. Integration reloads automatically when options change to apply blueprint changes

### Adding a New Optional Blueprint

To add a new optional blueprint, follow these steps:

#### 1. Create the Blueprint File
Create your blueprint YAML file in `blueprints/optional/`:
```bash
blueprints/optional/s42_my_new_blueprint.yaml
```

Ensure it follows the proper blueprint structure:
```yaml
blueprint:
  name: My Blueprint Name
  description: What this blueprint does
  domain: automation
  input:
    # Your inputs here

trigger:
  # Your triggers here

action:
  # Your actions here
```

#### 2. Register in `const.py`
Add configuration constants for your blueprint:

```python
# Optional Blueprints
CONF_BLUEPRINT_FRIENT_KEYPAD = "blueprint_frient_keypad"
CONF_BLUEPRINT_MY_NEW = "blueprint_my_new"  # <- Add this

# Default values
DEFAULT_BLUEPRINT_FRIENT_KEYPAD = False
DEFAULT_BLUEPRINT_MY_NEW = False  # <- Add this

# Optional blueprint mapping (filename -> config key)
OPTIONAL_BLUEPRINTS = {
    "s42_frient_keypad.yaml": CONF_BLUEPRINT_FRIENT_KEYPAD,
    "s42_my_new_blueprint.yaml": CONF_BLUEPRINT_MY_NEW,  # <- Add this
}
```

#### 3. Update `config_flow.py`
Import the new constants:
```python
from .const import (
    # ... existing imports ...
    CONF_BLUEPRINT_MY_NEW,
    DEFAULT_BLUEPRINT_MY_NEW,
)
```

Add the checkbox to the user step schema (around line 50):
```python
vol.Optional(
    CONF_BLUEPRINT_MY_NEW,
    default=DEFAULT_BLUEPRINT_MY_NEW,
): bool,
```

Add the checkbox to the options flow schema (around line 100):
```python
vol.Optional(
    CONF_BLUEPRINT_MY_NEW,
    default=options.get(
        CONF_BLUEPRINT_MY_NEW, DEFAULT_BLUEPRINT_MY_NEW
    ),
): bool,
```

#### 4. Add Translations

In `strings.json` (German), add to both `user` and `init` steps:
```json
"data": {
    "blueprint_my_new": "Meine neue Blueprint installieren"
},
"data_description": {
    "blueprint_my_new": "Beschreibung was diese Blueprint macht"
}
```

In `translations/en.json` (English):
```json
"data": {
    "blueprint_my_new": "Install My New Blueprint"
},
"data_description": {
    "blueprint_my_new": "Description of what this blueprint does"
}
```

#### 5. Test
1. Restart Home Assistant
2. Go to Devices & Services → Homebase42 → Configure
3. Enable your new blueprint checkbox
4. Verify the blueprint file appears in `config/blueprints/automation/homebase42/`
5. Disable the checkbox and verify the file is deleted

### Blueprint Best Practices
- Use descriptive `!input` names that are self-explanatory
- Provide good descriptions for all inputs
- Include default values where sensible
- Use selectors appropriate for the input type (entity, action, text, number, etc.)
- Add a `source_url` pointing to documentation if available
- Test with `mode: parallel` if blueprint might run concurrently
- Use proper YAML indentation (2 spaces)
- Keep `trigger` and `action` at root level, NOT under `blueprint`
