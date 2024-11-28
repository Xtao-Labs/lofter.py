from lofter.client.base import BaseClient
from lofter.client.routes import TAG_ANDROID_URL
from lofter.utils.enums import TagType

__all__ = ("AndroidTagClient",)


class AndroidTagClient(BaseClient):
    async def get_android_tag_posts(
        self,
        name: str,
        tag_type: TagType = TagType.NEW,
        starting_index: int = 0,
    ):
        url = TAG_ANDROID_URL
        payload = {
            "tag": name,
            "offset": starting_index,
            "type": tag_type.value,
            "recentDay": 0,
            "range": 0,
            "protectedFlag": 0,
            "postTypes": "",
            "postYm": "",
        }
        text = (await self.request_android("POST", url, data=payload)).text
        return text
