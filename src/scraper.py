import time
from typing import Generator
import logging
from datetime import datetime
from random import randint

from requester import Requester
from utils import *
from config import Config
from processor import Processor
from saver import Saver


class Scraper:
    """Scraps news articles from [Prothom Alo](https://www.prothomalo.com/) website."""

    def __init__(self, config_file_path: str) -> None:
        self.config = Config(config_file_path)
        self.logger: logging.Logger = setup_logger(
            logger_name="Scraper",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )
        self.requester = Requester(self.config)
        self.processor = Processor(self.config)
        self.saver = Saver(self.config)

    def begin(self):
        """Initiates scraping procedure."""
        for date_start in self.date_iterable():
            date_end = date_start + self.config.time_delta
            date_range_string = self.construct_date_range_string(
                date_start,
                date_end
            )

            try:
                self.logger.info(f"Working date range: {date_range_string}")
                self.fetch_articles_in_date_range(date_start, date_end)
            except Exception:
                self.logger.warning(f"No artciles in {date_range_string}")

    def construct_date_range_string(self, date_start: datetime, date_end: datetime) -> str:
        """Constructs date range string.

        Example: "01-01-2020 to 02-01-2020"

        Args:
            current_date (datetime): starting date.
            next_date (datetime): ending date.

        Returns:
            str: date range string.
        """
        string_start = date_to_string(date_start)
        string_end = date_to_string(date_end)
        return f"{string_start} to {string_end}"

    def fetch_articles_in_date_range(self, date_start: datetime, date_end: datetime) -> None:
        """Fetchs articles within `date_start` and `date_end`.

        # Parameters
            `date_start` (datetime): Earliest date of publication.
            `date_end` (datetime): Latest date of publication.

        # Raises
            Exception: Raised if response object is None.
        """
        for offset in self.offset_iterable():
            response = self.requester(date_start, date_end, offset)

            if int(response["total"]) is 0 or len(response["items"]) is 0:
                self.logger.info("response total is 0. Exiting loop.")
                break

            processed_items = self.processor(response["items"])
            self.saver(processed_items, date_start)
            self.config.update(
                newly_added=len(processed_items),
                last_scrapped_date=date_end
            )

            self.logger.info(f"Total scraped: {self.config.total}")

    def random_sleep(self):
        """Sleep for a random amount of time within range 
        `self.config.min_sleep_time` and `self.config.max_sleep_time`."""
        sleep_time: int = randint(
            self.config.min_sleep_time,
            self.config.max_sleep_time
        )
        self.logger.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

    def date_iterable(self) -> Generator[datetime, None, None]:
        """Creates a workable date range iterable.

        Workable date range always starts at `config.last_scraped_date` and 
        ends at `datetime.now()`.

        Yields:
            Generator[datetime, None, None]: Yields current date being scraped.
        """
        current_date = self.config.last_scraped_date

        while current_date < datetime.now():
            yield current_date
            current_date += self.config.time_delta

        self.logger.info("Reached current date. Exiting.")

    def offset_iterable(self) -> Generator[int, None, None]:
        """An offset iterable that increases offset value as many times it's called.

        The amount of offset increase is determined by the value of `self.config.limit`

        Yields:
            Generator[int, None, None]: Current offset value.
        """
        offset: int = 0

        while True:
            yield offset
            offset += self.config.limit


if __name__ == "__main__":
    scraper = Scraper("config.json")
    scraper.begin()
