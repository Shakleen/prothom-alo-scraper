import logging
import re
from typing import Dict, List, Tuple

from config import Config
from models import *
from utils import setup_logger


class Processor:
    """Processes raw response json data."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Processor",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )

    def __call__(self, items_in: List[Dict]) -> ItemsModel:
        self.logger.debug(f"Raw unprocessed items: {len(items_in)}")
        items_out = ItemsModel()

        for raw_item in items_in:
            items_out.add(self.parse_data(raw_item))

        self.logger.debug(f"Filtered processed items: {len(items_out)}")
        return items_out

    def parse_data(self, item: Dict) -> ItemModel:
        """Parse article data into `ItemModel`.

        # Parameters
            `item` (Dict): Raw news article data.

        # Returns
            ItemModel: Parsed news article data.
        """
        headline = item.get("headline", None)
        main_author = item.get("author-name", None)
        summary = item.get("summary", None)
        subheadline = item.get("subheadline", None)
        url = item.get("url", None)
        read_time = int(item.get("read-time", '0'))
        word_count = item.get("word-count", 0)
        id = item.get("id", None)
        tags = self.construct_tags_text(item)
        content = self.construct_content_text(item)
        created_at = self.to_unix_timestamp(
            item.get("created-at", 0)
        )
        published_at = self.to_unix_timestamp(
            item.get("published-at", 0)
        )
        updated_at = self.to_unix_timestamp(
            item.get("updated-at", 0)
        )
        last_published_at = self.to_unix_timestamp(
            item.get("last-published-at", 0)
        )
        first_published_at = self.to_unix_timestamp(
            item.get("first-published-at", 0)
        )
        content_updated_at = self.to_unix_timestamp(
            item.get("content-updated-at", 0)
        )
        seo_description, seo_tags = self.parse_seo_data(item)
        authors = self.construct_authors_text(item)
        sections = self.construct_sections_text(item)

        return ItemModel(
            headline=headline,
            subheadline=subheadline,
            content=content,
            tags=tags,
            published_at=published_at,
            url=url,
            seo_description=seo_description,
            seo_tags=seo_tags,
            main_author=main_author,
            authors=authors,
            summary=summary,
            read_time=read_time,
            id=id,
            sections=sections,
            word_count=word_count,
            created_at=created_at,
            updated_at=updated_at,
            first_published_at=first_published_at,
            last_published_at=last_published_at,
            content_updated_at=content_updated_at,
        )

    def to_unix_timestamp(self, timestamp_string: Dict) -> int:
        """Converts timestamp string to UNIX timestamp in seconds.

        Args:
            item (Dict): Raw news article data.

        Returns:
            int: UNIX Timestamp in seconds.
        """
        return int(int(timestamp_string) / 1000)

    def construct_authors_text(self, item: Dict) -> str:
        """Constructs comma separated author names.

        Args:
            item (Dict): Raw news article data.

        Returns:
            str: Comma separated author text.
        """
        authors: List[Dict] = item.get("authors", None)

        if authors is not None:
            authors = ",".join([
                str(author.get("name", ""))
                for author in authors
            ])

        return authors

    def parse_seo_data(self, item: Dict) -> Tuple[str, str]:
        """Parses SEO related data and returns relevant information.

        Args:
            item (Dict): Raw news article data.

        Returns:
            Tuple[str, str]: SEO Description and comma separated keywords.
        """
        description: str = None
        tags: str = None

        if "seo" in item.keys():
            description = item.get("meta-description", None)
            tags = item.get("meta-keywords", None)

        return description, tags

    def construct_content_text(self, item):
        return "".join([
            self.clean_text(element["text"])
            for card in item["cards"]
            for element in card["story-elements"]
            if element["type"] == "text"
        ])

    def construct_tags_text(self, item: Dict) -> str:
        """Constructs tag string.

        # Parameters
            `item` (Dict): Raw news article data.

        # Returns
            str: Comma separated tags.
        """
        tags: List[Dict] = item.get("tags", None)

        if tags is not None:
            tags = [
                tag.get("name", None)
                for tag in tags
            ]
            tags = ",".join(
                tag
                for tag in tags
                if tag is not None
            )

        return tags

    def clean_text(self, text: str) -> str:
        """Removes HTML tags from `text` string.

        # Parameters
            `text` (str): input text to be cleaned.

        # Returns
            str: Cleaned text.
        """
        cleaner = re.compile("<.*?>|&.*;")
        return re.sub(cleaner, "", text)

    def construct_sections_text(self, item: Dict) -> str:
        """Constructs sections string.

        # Parameters
            `item` (Dict): Raw news article data.

        # Returns
            str: Comma separated section names.
        """
        sections: List[Dict] = item.get("sections", None)

        if sections is not None:
            sections = [
                section.get("name", None)
                for section in sections
            ]
            tags = ",".join(
                section
                for section in sections
                if section is not None
            )

        return tags
