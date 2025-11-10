import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Path to the log file
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create a logger instance
logger = logging.getLogger("email_service")
logger.setLevel(logging.INFO)

# Create rotating file handler (1MB per file, 3 backups)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)

# Define how each log line looks
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(handler)
