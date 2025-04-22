import logging
import inspect

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def log_internal_server_error(EXCEPTION):
    """
    Log internal server errors that could occur when a client requests a resource.

    Parameters:
        EXCEPTION (Exception): The exception to log.
    """
    logger.exception(f'An Internal Server Error was thrown as a result of an exception in "{inspect.stack()[1].function}": {EXCEPTION}')