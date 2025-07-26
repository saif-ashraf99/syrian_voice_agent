import logging

# Configure logging for orders module
logging.basicConfig(level=logging.INFO)

# Order configuration
ORDER_ID_LENGTH = 8
MIN_ETA_MINUTES = 15
MAX_ETA_MINUTES = 45

# Valid order statuses
VALID_ORDER_STATUSES = ['confirmed', 'preparing', 'ready', 'delivered', 'cancelled']

# Currency settings
DEFAULT_CURRENCY = 'USD'