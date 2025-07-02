import pytest
import pytest_asyncio

from lofter.client.lofter import LofterClient


@pytest_asyncio.fixture
async def lofter_client(login_auth_key: str):
    async with LofterClient(login_auth_key=login_auth_key) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestLofterClient:
    @staticmethod
    async def test_tag(lofter_client: "LofterClient"):
        assert lofter_client.client
        req = await lofter_client.get_web_tag_posts("基尼奇")
        assert len(req) > 0
        req2 = await lofter_client.get_android_tag_posts("基尼奇")
