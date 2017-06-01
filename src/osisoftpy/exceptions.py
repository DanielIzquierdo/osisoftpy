# -*- coding: utf-8 -*-

"""
osisoftpy.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of OSIsoftPy's exceptions.
"""


# TODO: Implement custom PI Web API HTTP response codes:
# streams/{webid}/GetInterpolated
# 200: The values that meet the specified conditions.
# 400: The request was malformed.
# 409: The data reference does not support this method,
#      or the supplied filter expression is unsupported,
#      or the desired units of measure are incompatible.


class OSIsoftPyException(Exception):
    """There was an ambiguous exception while handling your request."""
    pass


class PIWebAPIError(OSIsoftPyException):
    pass


class HTTPError(OSIsoftPyException):
    """An HTTP error occurred."""


class Unauthorized(HTTPError):
    """401 unauthorized"""


class ConnectionError(OSIsoftPyException):
    """A Connection error occurred."""


class ProxyError(ConnectionError):
    """A proxy error occurred."""


class SSLError(ConnectionError):
    """An SSL error occurred."""


class Timeout(OSIsoftPyException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~osisoftpy.exceptions.ConnectTimeout` and
    :exc:`~osisoftpy.exceptions.ReadTimeout` errors.
    """


class ConnectTimeout(ConnectionError, Timeout):
    """The request timed out while trying to webapi to the remote server.

    Requests that produced this error are safe to retry.
    """


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""


class URLRequired(OSIsoftPyException):
    """A valid URL is required to make a request."""


class TooManyRedirects(OSIsoftPyException):
    """Too many redirects."""


class MissingSchema(OSIsoftPyException, ValueError):
    """The URL schema (e.g. http or https) is missing."""


class InvalidSchema(OSIsoftPyException, ValueError):
    """See defaults.py for valid schemas."""


class InvalidURL(OSIsoftPyException, ValueError):
    """The URL provided was somehow invalid."""


class InvalidHeader(OSIsoftPyException, ValueError):
    """The header value provided was somehow invalid."""


class ChunkedEncodingError(OSIsoftPyException):
    """The server declared chunked encoding but sent an invalid chunk."""


class StreamConsumedError(OSIsoftPyException, TypeError):
    """The content for this response was already consumed"""


class RetryError(OSIsoftPyException):
    """Custom retries logic failed"""


class UnrewindableBodyError(OSIsoftPyException):
    """OSIsoftPy encountered an error when trying to rewind a body"""

class MismatchEntriesError(OSIsoftPyException):
    """Two lists are mismatched"""

# Warnings


class OSIsoftPyWarning(Warning):
    """Base warning for OSIsoftPy."""
    pass


class FileModeWarning(OSIsoftPyWarning, DeprecationWarning):
    """A file was opened in text mode, but OSIsoftPy determined its binary
    length."""
    pass
