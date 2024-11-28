from typing import Union
from urllib.parse import urljoin

from httpx import URL as _URL

URLTypes = Union["URL", str]


class URL(_URL):
    """A subclass of httpx's URL class, with additional convenience methods for URL manipulation."""

    def join(self, url: URLTypes) -> "URL":
        """
        Join the current URL with the given URL.

        Args:
            url (Union[URL, str]): The URL to join with.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self), str(URL(url))))

    def __truediv__(self, url: URLTypes) -> "URL":
        """
        Append the given URL to the current URL using the '/' operator.

        Args:
            url (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self) + "/", str(URL(url))))

    def __bool__(self):
        """Return True if the URL is not empty.

        Returns:
            bool: True if the URL is not empty.

        """
        return str(self) != ""

    def replace(self, old: str, new: str) -> "URL":
        """
        Replace a substring in the URL.

        Args:
            old (str): The substring to replace.
            new (str): The new substring to replace with.

        Returns:
            URL: A new URL instance with the substring replaced.

        """
        return URL(str(self).replace(old, new))


class BaseRoute:
    """A base class for defining routes with useful metadata."""


class Route(BaseRoute):
    """A standard route with a single URL."""

    url: URL

    def __init__(self, url: str) -> None:
        """
        Initialize a Route instance.

        Args:
            url (str): The URL for this route.

        """
        self.url = URL(url)

    def get_url(self) -> URL:
        """
        Get the URL for this route.

        Returns:
            URL: The URL for this route.

        """
        return self.url

    def __truediv__(self, other: str) -> URL:
        """
        Append the given URL to this route using the '/' operator.

        Args:
            other (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return self.url / other


ROOT_URL = Route("https://www.lofter.com")
API_URL = Route("https://api.lofter.com")

TAG_URL = ROOT_URL / "dwr/call/plaincall/TagBean.getCommonTagExcellentAuthors.dwr"
TAG_ANDROID_URL = API_URL / "newapi/tagPosts.json"
