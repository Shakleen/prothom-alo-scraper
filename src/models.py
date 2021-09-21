from dataclasses import dataclass
from typing import List


@dataclass
class ItemModel:
    """Holds information related to a single news article."""

    headline: str = None
    subheadline: str = None
    content: str = None
    tags: str = None
    published_at: int = None
    created_at: int = None
    updated_at: int = None
    last_published_at: int = None
    first_published_at: int = None
    content_updated_at: int = None
    seo_description: str = None
    seo_tags: str = None
    main_author: str = None
    authors: str = None
    url: str = None
    read_time: int = None
    summary: str = None
    sections: str = None
    id: str = None
    word_count: int = None

    def to_list(self) -> List:
        return [
            self.id,
            self.headline,
            self.subheadline,
            self.summary,
            self.content,
            self.main_author,
            self.authors,
            self.url,
            self.read_time,
            self.seo_description,
            self.seo_tags,
            self.tags,
            self.sections,
            self.word_count,
            self.published_at,
            self.first_published_at,
            self.last_published_at,
            self.created_at,
            self.updated_at,
            self.content_updated_at,
        ]


class ItemsModel:
    """Holds data for multiple news articles in a list."""

    COLUMN_NAMES: List[str] = [
        "text_id",
        "text_headline",
        "text_subheadline",
        "text_summary",
        "text_content",
        "text_main_author",
        "text_authors",
        "text_url",
        "int_read_time",
        "text_seo_description",
        "text_seo_tags",
        "text_tags",
        "text_sections",
        "int_word_count",
        "date_published",
        "date_first_published_at",
        "date_last_published_at",
        "date_created_at",
        "date_updated_at",
        "date_content_updated_at",
    ]

    def __init__(self) -> None:
        self.items: List[ItemModel] = []

    def add(self, item: ItemModel):
        if self.is_acceptable(item):
            self.items.append(item)

    def __len__(self) -> int:
        """Returns the number of parsed articles."""
        return len(self.items)

    def is_acceptable(self, item: ItemModel) -> bool:
        """Checks whether `item` is acceptable.

        An item is acceptable iff it has a non-null and non-empty 
        headline and content.

        # Parameters
            `item` (ItemModel): News article data.

        # Returns
            bool: True if the item should be added. False otherwise.
        """
        if item.headline is not None and item.content is not None:
            return len(item.headline) and len(item.content)

        return False

    def to_list(self) -> List:
        return [
            item.to_list()
            for item in self.items
        ]
