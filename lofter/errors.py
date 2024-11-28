class LofterException(Exception):
    """Base class for Lofter errors."""


class NetworkError(LofterException):
    """Base class for exceptions due to networking errors."""


class TimedOut(NetworkError):
    """Raised when a request took too long to finish."""
