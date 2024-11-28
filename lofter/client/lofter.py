from lofter.client.components.android.tag import AndroidTagClient
from lofter.client.components.web.tag import WebTagClient

__all__ = ("LofterClient",)


class LofterClient(
    WebTagClient,
    AndroidTagClient,
):
    """A simple http client for lofter endpoints."""
