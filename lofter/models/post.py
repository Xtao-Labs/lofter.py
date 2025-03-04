import datetime
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from lofter.models.artwork import ArtWorkImage
from lofter.models.author import BlogInfo


class PhotoLink(ArtWorkImage):
    url: str = Field(alias="orign")


class PhotoPostView(BaseModel):
    id: int
    blogId: int
    caption: str
    photoLinks: List[PhotoLink]
    photoCaptions: List[str]
    photoType: int
    firstImage: PhotoLink


class VideoInfo(ArtWorkImage):
    video_img_url: str
    url: str = Field(alias="originUrl")


class VideoPostView(BaseModel):
    id: int
    blogId: int
    caption: str
    videoInfo: VideoInfo
    videoType: int
    videoCreateTime: datetime.datetime
    playCount: int


class PostType(IntEnum):
    TEXT = 1
    PHOTO = 2
    VIDEO = 4


class PostView(BaseModel):
    id: int
    blogId: int
    title: str
    type: int
    publishTime: datetime.datetime

    digest: str
    tagList: List[str]

    permalink: str

    photoCount: int
    ccType: int
    createTime: datetime.datetime

    photoPostView: Optional[PhotoPostView] = None
    videoPostView: Optional[VideoPostView] = None


class PostCountView(BaseModel):
    blogId: int
    responseCount: int
    favoriteCount: int
    reblogCount: int
    shareCount: int
    viewCount: int
    hotCount: int
    subscribeCount: int


class BlogPostData(BaseModel):
    postView: PostView
    postCountView: PostCountView


class BlogPost(BaseModel):
    blogInfo: BlogInfo
    postData: BlogPostData
