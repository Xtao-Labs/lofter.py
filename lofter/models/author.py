from pydantic import BaseModel, Field


class Author(BaseModel):
    auther_id: int
    name: str
    url: str


class BlogInfo(Author):
    auther_id: int = Field(alias="blogId")
    name: str = Field(alias="blogNickName")
    url: str = Field(alias="bigAvaImg")
