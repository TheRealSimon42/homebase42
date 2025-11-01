"""Constants for the Homebase42 integration."""

DOMAIN = "homebase42"
NAME = "Homebase42"

# Config flow constants
CONF_BATTERY_CRITICAL_THRESHOLD = "battery_critical_threshold"
CONF_BATTERY_LOW_THRESHOLD = "battery_low_threshold"
CONF_UNAVAILABLE_NOTIFICATION_DELAY = "unavailable_notification_delay"
CONF_INCLUDE_HIDDEN_ENTITIES = "include_hidden_entities"

# Optional Blueprints
CONF_BLUEPRINT_FRIENT_KEYPAD = "blueprint_frient_keypad"

# Default values
DEFAULT_BATTERY_CRITICAL = 20
DEFAULT_BATTERY_LOW = 50
DEFAULT_UNAVAILABLE_DELAY = 3  # hours
DEFAULT_INCLUDE_HIDDEN_ENTITIES = False
DEFAULT_BLUEPRINT_FRIENT_KEYPAD = False

# Attributes
ATTR_ENTITIES = "entities"
ATTR_COUNT = "count"
ATTR_LAST_UPDATED = "last_updated"

# Blueprint directories
BLUEPRINTS_CORE = "core"
BLUEPRINTS_OPTIONAL = "optional"

# Optional blueprint mapping (filename -> config key)
OPTIONAL_BLUEPRINTS = {
    "s42_frient_keypad.yaml": CONF_BLUEPRINT_FRIENT_KEYPAD,
}
