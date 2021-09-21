import logging
import time
from datetime import datetime
from typing import Dict
import requests

from config import Config
from utils import setup_logger


class Requester:
    """Fetches response from Prothom Alo website and returns json data."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Requester",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )

    @property
    def url_format(self) -> str:
        """Prothom Alo API url format.

        Four parameters should be provided to use this url which are as follows:
        1. `offset`
        2. `limit`
        3. `start`
        4. `end`
        """
        return (
            "https://www.prothomalo.com/api/v1/advanced-search?"
            + "offset={offset}&limit={limit}&sort=latest-published"
            + "&published-after={start}&published-before={end}"
        )

    def __call__(
        self,
        date_start: datetime,
        date_end: datetime,
        offset: int,
    ) -> Dict:
        """Fetches response json data.

        Fetches news article data that was published with in [`date_start`, `date_end`] 
        and at `offset`.

        # Parameters
            `date_start` (datetime): Minimum date of publication.
            `date_end` (datetime): Maximum date of publication.
            `end_timestamp` (int): Offset value.

        # Raises:
            Exception: Raised when all request attempts failed.

        # Returns
            Dict: response json data.
        """
        for attempt in range(1, self.config.max_attempts+1):
            try:
                request_url = self.construct_request_url(
                    date_start,
                    date_end,
                    offset
                )
                response = requests.get(request_url)
                return response.json()
            except Exception:
                self.logger.warning(f"Attempt {attempt}: Request failed.")
                self.wait(attempt)

        raise Exception("All request attempts failed.")

    def wait(self, attempt: int):
        """Waits a certain amount of time after a request fails.

        The larger the `attempt` value the longer we wait.

        Args:
            attempt (int): Attempt number.
        """
        sleep_time = 30 * attempt
        self.logger.log(f"Attempting {attempt+1}th time in {sleep_time}s.")
        time.sleep(sleep_time)

    def construct_request_url(
        self,
        date_start: datetime,
        date_end: datetime,
        offset: int
    ) -> str:
        """Constructs request URL using appropriate values.

        Args:
            date_start (datetime): Earliest published date an article can have.
            date_end (datetime): Latest publish date an article can have.
            offset (int): Amount of offset to use.

        Returns:
            str: Constructed request url.
        """
        request_url = self.url_format.format(
            offset=offset,
            limit=self.config.limit,
            start=self.date_to_unix_timestamp(date_start),
            end=self.date_to_unix_timestamp(date_end)
        )
        self.logger.info(f"Request URL: {request_url}")
        return request_url

    def date_to_unix_timestamp(self, time: datetime) -> int:
        """Converts `time` to unix timestamp in milliseconds.

        Args:
            time (datetime): Time to be converted.

        Returns:
            int: Unix timestamp in milliseconds.
        """
        return int(time.timestamp() * 1000)

# https://www.prothomalo.com/api/v1/advanced-search?offset=0&limit=5&sort=latest-published&published-after=1632051372388&published-before=1632137772388
