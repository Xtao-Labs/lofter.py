import json
from typing import List, Optional

from lofter.models.artwork import ArtWork, ArtWorkImage
from lofter.models.author import Author


def get_web_tag_author(_post: dict) -> Optional[Author]:
    _author = _post.get("blogInfo")
    if not _author:
        return
    return Author(
        auther_id=_author.get("blogId"),
        name=_author.get("blogNickName"),
        url=_author.get("homePageUrl"),
    )


def rewrite_image_url(url: str) -> str:
    return url.split("?")[0]


def get_web_tag_image(_post: dict) -> List[ArtWorkImage]:
    data = []
    # video
    if _embed := _post.get("embed"):
        embed = json.loads(_embed.replace("'", '"'))
        url = embed.get("h256Url") or embed.get("video_down_url")
        if url:
            data.append(
                ArtWorkImage(
                    url=url,
                    video_first_img=embed.get("video_img_url")
                    or embed.get("video_first_img"),
                    size=embed.get("size"),
                )
            )
    # photo gif
    if _photo_links := _post.get("photoLinks"):
        photo_links = json.loads(_photo_links.replace("'", '"'))
        for p in photo_links:
            if orign := p.get("orign"):
                data.append(ArtWorkImage(url=rewrite_image_url(orign)))
    return data


def get_web_tag_post(data: dict) -> Optional[ArtWork]:
    _post = data.get("post")
    if not _post:
        return
    author = get_web_tag_author(_post)
    images = get_web_tag_image(_post)
    return ArtWork(
        blog_id=_post.get("id"),
        title=_post.get("title"),
        url=_post.get("blogPageUrl"),
        images=images,
        tags=_post.get("tagList"),
        create_time=_post.get("publishTime"),
        author=author,
    )


def get_web_tag_posts(post_data: list[dict]) -> List[ArtWork]:
    data = []
    for d in post_data:
        if not d:
            continue
        if i := get_web_tag_post(d):
            data.append(i)
    return data
