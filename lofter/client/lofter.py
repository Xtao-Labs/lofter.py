from lofter.client.components.android.tag import AndroidTagClient
from lofter.client.components.web.post import WebPostClient
from lofter.client.components.web.tag import WebTagClient

__all__ = ("LofterClient",)


class LofterClient(
    WebPostClient,
    WebTagClient,
    AndroidTagClient,
):
    """A simple http client for lofter endpoints."""
