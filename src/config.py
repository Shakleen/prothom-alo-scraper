from datetime import timedelta
import os
from typing import Any, Dict

import json

from utils import *


_ERROR_MSG_INVALID_OUTPUT = "Output path doesn't exist!"
_ERROR_MSG_OUTPUT_NOT_DIR = "Output path must be a directory"


class Config:
    """Holds configuration data from "config.json" file."""

    def __init__(self, config_file_path: str) -> None:
        assert os.path.exists(
            config_file_path), f"Config file not found at {config_file_path}"
        assert self.is_json_file(
            config_file_path), f"Config file at {config_file_path} is not a json file"
        self.config_file_path: str = config_file_path

        with open(self.config_file_path) as config_fp:
            self.configs: Dict[str, Any] = json.load(config_fp)

        assert os.path.exists(
            self.output_dir), f"Output path {self.output_dir} doesn't exist!"
        assert os.path.isdir(
            self.output_dir), f"Output path {self.output_dir} is not a directory"

    @property
    def last_scraped_date(self) -> datetime:
        """Last date upto which news articles were scrapped (starting from `start_date`). 

        Must follow format DD-MM-YYYY e.g. 21-01-2010."""
        if self.configs["last_scraped_date"]["value"] is not None:
            return string_to_date(
                self.configs["last_scraped_date"]["value"]
            )

        return string_to_date(
            self.configs["start_date"]["value"]
        )

    @property
    def log_level(self) -> int:
        """Log level of Python Logger.

        10 - Log DEBUG and above.
        20 - Log INFO and above.
        30 - Log WARNING and above.
        40 - Log ERROR and above.
        50 - Log CRITICAL and above.
        """
        return self.configs["log_level"]["value"]

    @property
    def log_message_format(self) -> str:
        """Log format for Python logger."""
        return self.configs["log_message_format"]["value"]

    @property
    def time_delta(self) -> timedelta:
        """Number of days whose articles should be fetched together."""
        return timedelta(days=int(self.configs["threshold"]["value"]))

    @property
    def limit(self) -> int:
        """Number of articles to fetch in one request."""
        return self.configs["limit"]["value"]

    @property
    def total(self) -> int:
        """Number of articles scrapped so far."""
        return self.configs["total"]["value"]

    @property
    def max_attempts(self) -> int:
        """Max number of attempts a request can fail before moving on."""
        return self.configs["max_attempts"]["value"]

    @property
    def output_dir(self) -> str:
        """Directory path where news articles are to be saved."""
        return self.configs["output_directory"]["value"]

    @property
    def min_sleep_time(self) -> int:
        """Minimum number of seconds the scraper must sleep in between requests."""
        return self.configs["min_sleep_time"]["value"]

    @property
    def max_sleep_time(self) -> int:
        """Maximum number of days to go without finding a single news article."""
        return self.configs["max_sleep_time"]["value"]

    @property
    def log_file_path(self) -> str:
        """File path to which log messages will be saved.

        The log file will have a prefix of time in the format
        DD-MM-YYYY hh-mm-ss (AM or PM). 
        
        Example: 21-01-2021 11:12:13 AM.log
        """
        log_dir = self.configs["log_directory"]["value"]

        if not hasattr(self, "log_file_name"):
            format_string: str = "%d-%m-%Y %I-%M-%S %p"
            time_prefix_string: str = datetime.now().strftime(format_string)
            self.log_file_name: str = f"{time_prefix_string}.log"

        return os.path.join(log_dir, self.log_file_name)

    def update(self, newly_added: int, last_scrapped_date: datetime) -> None:
        """Update config file with last scraped date and total scraped information.

        Args:
            added (int): New articles added.
            last_scrapped_date (datetime): Last date upto which articles were scrapped.
        """
        self.configs["total"]["value"] += newly_added
        self.configs["last_scraped_date"]["value"] = date_to_string(
            last_scrapped_date
        )

        with open(self.config_file_path, "w") as config_fp:
            json.dump(self.configs, config_fp)

    def __repr__(self) -> str:
        return "\n".join([
            dic["description"] + "\n\tCurrent Value: " +
            str(dic["value"]) + "\n"
            for dic in self.configs.values()
        ])

    def is_json_file(self, path: str) -> bool:
        """Checks whether the file at `path` is a json file.

        The checking is performed by matching the extension of the file. Meaning,
        the function checks whether the file has ".json" extension at the end.

        ### Example
        >>> is_json_file("path/to/file.json")
        True
        >>> is_json_file("path/to/file.yaml")
        False

        ### Parameters
            `path` (str): File name or file path.

        ### Returns
            bool: True if is of type json, otherwise False.
        """
        file_extension = path.split(".")[-1].lower()
        return file_extension == "json"

if __name__ == "__main__":
    CONFIG_FILE_PATH = "config.json"

    config = Config(CONFIG_FILE_PATH)
    print(config)
    config.update(newly_added=10, last_scrapped_date=datetime.now())
