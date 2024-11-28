from datetime import datetime, timezone
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel

from lofter.models.author import Author


class ImageType(IntEnum):
    STATIC = 1
    GIF = 2
    VIDEO = 3
    TEXT = 4


class ArtWorkImage(BaseModel):
    url: str
    video_first_img: Optional[str] = None
    size: Optional[int] = None

    @property
    def format_url(self) -> str:
        return self.url + "?imageView&thumbnail=1920x0&quality=90&stripmeta=0&type=jpg"

    @property
    def type(self) -> ImageType:
        if self.url.endswith(".gif"):
            return ImageType.GIF
        if ".mp4" in self.url:
            return ImageType.VIDEO
        return ImageType.STATIC


class ArtWork(BaseModel):
    web_name: str = "Lofter"
    blog_id: int
    title: str
    url: str
    images: List[ArtWorkImage]
    tags: Optional[List[str]] = None
    create_time: datetime
    author: Author
    nsfw: bool = False

    def format_tags(self) -> str:
        return " ".join(f"#{tag}" for tag in self.tags)

    def get_create_time_timestamp(self) -> int:
        return int(self.create_time.replace(tzinfo=timezone.utc).timestamp())

    def format_text(self) -> str:
        return (
            f"Title {self.title}\n"
            if self.title
            else ""
            f"Tag {self.format_tags()}\n"
            f"From <a href='{self.url}'>{self.web_name}</a> "
            f"By <a href='{self.author.url}'>{self.author.name}</a>\n"
            f"At {self.create_time.strftime('%Y-%m-%d %H:%M')}"
        )
