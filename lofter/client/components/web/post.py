import json
import re

from lofter.client.base import BaseClient

__all__ = ("WebPostClient",)

from lofter.errors import InvalidResponse
from lofter.models.post import BlogPost

from lofter.utils.post import get_blog_post_url


class WebPostClient(BaseClient):
    async def get_post_detail_web(
        self,
        blog_name: str,
        permalink: str,
    ):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        }
        url = get_blog_post_url(blog_name, permalink)
        text = (await self.request_web("GET", url, headers=headers)).text
        data = re.findall(r"window.__initialize_data__ = (.*?)</script>", text)
        if not data:
            raise InvalidResponse("Could not find post data.")
        json_data = json.loads(data[0].strip())
        return BlogPost(**json_data["postData"]["data"])
