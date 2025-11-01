"""Constants for the Homebase42 integration."""

DOMAIN = "homebase42"
NAME = "Homebase42"

# Config flow constants
CONF_BATTERY_CRITICAL_THRESHOLD = "battery_critical_threshold"
CONF_BATTERY_LOW_THRESHOLD = "battery_low_threshold"
CONF_UNAVAILABLE_NOTIFICATION_DELAY = "unavailable_notification_delay"
CONF_INCLUDE_HIDDEN_ENTITIES = "include_hidden_entities"
CONF_WEATHER_ENTITY = "weather_entity"

# Multi-step flow toggles
CONF_CONFIGURE_BLUEPRINTS = "configure_blueprints"
CONF_CONFIGURE_WEATHER = "configure_weather"

# Optional Blueprints
CONF_BLUEPRINT_FRIENT_KEYPAD = "blueprint_frient_keypad"

# Optional Templates
CONF_TEMPLATE_WEATHER = "template_weather"

# Default values
DEFAULT_BATTERY_CRITICAL = 20
DEFAULT_BATTERY_LOW = 50
DEFAULT_UNAVAILABLE_DELAY = 3  # hours
DEFAULT_INCLUDE_HIDDEN_ENTITIES = False
DEFAULT_WEATHER_ENTITY = "weather.forecast_home"
DEFAULT_CONFIGURE_BLUEPRINTS = False
DEFAULT_CONFIGURE_WEATHER = False
DEFAULT_BLUEPRINT_FRIENT_KEYPAD = False
DEFAULT_TEMPLATE_WEATHER = False

# Attributes
ATTR_ENTITIES = "entities"
ATTR_COUNT = "count"
ATTR_LAST_UPDATED = "last_updated"

# Blueprint directories
BLUEPRINTS_CORE = "core"
BLUEPRINTS_OPTIONAL = "optional"

# Template directories
TEMPLATES_OPTIONAL = "optional"

# Optional blueprint mapping (filename -> config key)
OPTIONAL_BLUEPRINTS = {
    "s42_frient_keypad.yaml": CONF_BLUEPRINT_FRIENT_KEYPAD,
}

# Optional template mapping (filename -> config key)
OPTIONAL_TEMPLATES = {
    "s42_weather_forecasts.yaml": CONF_TEMPLATE_WEATHER,
}

# Repair issues
REPAIR_RESTART_REQUIRED = "restart_required_templates"
