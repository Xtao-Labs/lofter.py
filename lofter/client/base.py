import logging
from types import TracebackType
from typing import AsyncContextManager, Type, Optional, Any

from httpx import AsyncClient, TimeoutException, Response, HTTPError, Timeout, Headers

from lofter.client.routes import URLTypes
from lofter.errors import TimedOut, NetworkError
from lofter.utils.types import RequestData, QueryParamTypes, HeaderTypes

_LOGGER = logging.getLogger("lofter.BaseClient")

__all__ = ("BaseClient",)


class BaseClient(AsyncContextManager["BaseClient"]):
    """
    This is the base class for lofter clients. It provides common methods and properties for lofter clients.

    Args:
        timeout (Optional[TimeoutTypes], optional): Timeout configuration for the client.
    """

    def __init__(
        self,
        timeout: int = None,
    ) -> None:
        """Initialize the client with the given parameters."""
        if timeout is None:
            timeout = Timeout(
                connect=5.0,
                read=5.0,
                write=5.0,
                pool=1.0,
            )
        self.client = AsyncClient(timeout=timeout)

    async def __aenter__(self: "BaseClient") -> "BaseClient":
        """Enter the async context manager and initialize the client."""
        try:
            await self.initialize()
            return self
        except Exception as exc:
            await self.shutdown()
            raise exc

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit the async context manager and shutdown the client."""
        await self.shutdown()

    async def shutdown(self):
        """Shutdown the client."""
        if self.client.is_closed:
            _LOGGER.info("This Client is already shut down. Returning.")
            return

        await self.client.aclose()

    async def initialize(self):
        """Initialize the client."""

    @staticmethod
    def get_default_web_header(headers: HeaderTypes):
        """Get the default header for web requests.

        Args:
            headers (HeaderTypes): The header to use.

        Returns:
            Headers: The default header with added fields.
        """
        headers = Headers(headers)
        headers["user-agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
        headers["referer"] = "https://www.lofter.com"
        return headers

    @staticmethod
    def get_default_android_header(headers: HeaderTypes):
        """Get the default header for android requests.

        Args:
            headers (HeaderTypes): The header to use.

        Returns:
            Headers: The default header with added fields.
        """
        headers = Headers(headers)
        headers["user-agent"] = (
            "LOFTER-Android 8.0.15 (MI MAX 2; Android 15.0.0; null) WIFI"
        )
        return headers

    async def request(
        self,
        method: str,
        url: URLTypes,
        data: Optional[RequestData] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ) -> Response:
        """Make an HTTP request and return the response.

        This method makes an HTTP request with the specified HTTP method, URL, request parameters, headers,
        and JSON payload. It catches common HTTP errors and raises a `NetworkError` or `TimedOut` exception
        if the request times out.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            data (Optional[RequestData]): The request data to include in the body of the request.
            json (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Response: A `Response` object representing the HTTP response.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.

        """
        try:
            return await self.client.request(
                method,
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
            )
        except TimeoutException as exc:
            raise TimedOut from exc
        except HTTPError as exc:
            raise NetworkError from exc

    async def request_web(
        self,
        method: str,
        url: URLTypes,
        data: Optional[RequestData] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ):
        headers = headers or self.get_default_web_header(headers)
        return await self.request(method, url, data, json, params, headers)

    async def request_android(
        self,
        method: str,
        url: URLTypes,
        data: Optional[RequestData] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ):
        headers = headers or self.get_default_android_header(headers)
        return await self.request(method, url, data, json, params, headers)
