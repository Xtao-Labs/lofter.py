from urllib.parse import quote

from lofter.client.base import BaseClient
from lofter.client.routes import TAG_URL
from lofter.utils.dwr_parse import parse_dwr_string
from lofter.utils.enums import TagType

__all__ = ("WebTagClient",)


class WebTagClient(BaseClient):
    async def get_web_tag_posts(
        self,
        name: str,
        tag_type: TagType = TagType.NEW,
        page_size: int = 20,
        starting_index: int = 0,
    ):
        url = TAG_URL
        payload = {
            "callCount": 1,
            "scriptSessionId": "${scriptSessionId}187",
            "httpSessionId": "",
            "c0-scriptName": "TagBean",
            "c0-methodName": "search",
            "c0-id": "0",
            "c0-param0": f"string:{quote(name)}",
            "c0-param1": "number:0",
            "c0-param2": "string:",
            "c0-param3": f"string:{tag_type.value}",
            "c0-param4": "boolean:false",
            "c0-param5": "number:0",
            "c0-param6": f"number:{page_size}",
            "c0-param7": f"number:{starting_index}",
            "c0-param8": "number:0",
            "batchId": 493053,
        }
        text = (await self.request_web("POST", url, data=payload)).text
        return parse_dwr_string(text)
