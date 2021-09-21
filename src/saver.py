import os
import logging
from datetime import datetime

import pandas as pd

from config import Config
from models import ItemsModel
from utils import setup_logger


class Saver:
    """Saves processed news articles in disk in `output_dir`."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Saver",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )

    def __call__(self, items_in: ItemsModel, current_date: datetime) -> None:
        dataframe = pd.DataFrame(
            items_in.to_list(),
            columns=ItemsModel.COLUMN_NAMES,
        )
        output_file_path = self.construct_output_filepath(current_date)
        dataframe.to_csv(
            output_file_path,
            index=None,
            header=not os.path.exists(output_file_path),
            mode="a",
        )
        self.logger.info(f"Saved to file: {output_file_path}")

    def construct_output_filepath(self, current_date: datetime) -> str:
        """Helper function to get output csv file path.

        The name is of the format "<YEAR>".csv
        For example: 2021.csv

        # Parameters
            `current_date` (datetime): Current date being scraped.

        # Returns
            str: output csv file path.
        """
        date_str = current_date.strftime("%Y")
        file_name = f"{date_str}.csv"
        file_path = os.path.join(self.config.output_dir, file_name)
        return file_path
