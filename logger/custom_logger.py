import os
import logging
from datetime import datetime

def get_log_dir() -> str:
    """
    Returns the absolute path to the logs directory, creating it if it doesn't exist.
    
    Returns
    -------
    str
        The path to the logs directory.
    """
    log_dir: str = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def get_log_file_path(log_dir: str) -> str:
    """
    Generates a unique log file path based on the current datetime.

    Parameters
    ----------
    log_dir : str
        The directory where the log file will be stored.

    Returns
    -------
    str
        The full path to the log file.
    """
    log_file: str = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    return os.path.join(log_dir, log_file)

# Set up logging
LOG_DIR: str = get_log_dir()
LOG_FILE_PATH: str = get_log_file_path(LOG_DIR)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger: logging.Logger = logging.getLogger("my_agentic_app")