"""Constants for the Homebase42 integration."""

DOMAIN = "homebase42"
NAME = "Homebase42"

# Config flow constants
CONF_BATTERY_CRITICAL_THRESHOLD = "battery_critical_threshold"
CONF_BATTERY_LOW_THRESHOLD = "battery_low_threshold"
CONF_UNAVAILABLE_NOTIFICATION_DELAY = "unavailable_notification_delay"
CONF_INCLUDE_HIDDEN_ENTITIES = "include_hidden_entities"

# Default values
DEFAULT_BATTERY_CRITICAL = 20
DEFAULT_BATTERY_LOW = 50
DEFAULT_UNAVAILABLE_DELAY = 3  # hours
DEFAULT_INCLUDE_HIDDEN_ENTITIES = False

# Attributes
ATTR_ENTITIES = "entities"
ATTR_COUNT = "count"
ATTR_LAST_UPDATED = "last_updated"
