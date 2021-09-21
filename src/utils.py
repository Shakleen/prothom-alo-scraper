from datetime import datetime
import logging


def setup_logger(
    logger_name: str,
    log_file_path: str,
    log_level: int,
    log_message_format: str,
) -> logging.Logger:
    """Function to create a logger object to use in logging messages to a file.

    ### Parameters
        `logger_name` (str): Name of the logger.
        `log_file_path` (str): File path to which logs should be saved.
        `log_level` (int): Logging level.
        `log_message_format` (str): Log message format.

    ### Returns
        logging.Logger: Built logger.
    """
    logger: logging.Logger = logging.getLogger(logger_name)

    formatter = logging.Formatter(log_message_format)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(log_level)

    return logger


def string_to_date(date_str: str) -> datetime:
    """Converts date string of format "%d-%m-%Y" to `datetime` object.

    # Parameters
        `date_string` (str): Date time string.

    # Returns
        datetime: Converted date time as datetime object.
    """
    return datetime.strptime(date_str, "%d-%m-%Y")


def date_to_string(date: datetime) -> str:
    """Converts `datetime` object to string of format "%d-%m-%Y"

    # Parameters
        `date` (datetime): Input date.

    # Returns
        str: Formatted date string.
    """
    return date.strftime("%d-%m-%Y")
