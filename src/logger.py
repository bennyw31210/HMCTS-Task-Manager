import logging
import inspect

# Set up the base logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# Create a formatter
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a console handler (for printing to terminal)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

# Create a file handler (for writing to a file)
FILE_HANDLER = logging.FileHandler('app.log')  # <-- 'app.log' is the file name
FILE_HANDLER.setFormatter(FORMATTER)

# Add handlers to the logger
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

def log_internal_server_error(EXCEPTION):
    """
    Log internal server errors that could occur when a client requests a resource.

    Parameters:
        EXCEPTION (Exception): The exception to log.
    """
    LOGGER.exception(f'An Internal Server Error was thrown as a result of an exception in "{inspect.stack()[1].function}": {EXCEPTION}')
