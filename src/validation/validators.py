# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
# |																|
# |             Copyright 2023 - 2023, Amulya Paritosh			|
# |																|
# |  This file is part of Component Library Plugin for FreeCAD.	|
# |																|
# |               This file was created as a part of				|
# |              Google Summer Of Code Program - 2023			|
# |																|
# --------------------------------------------------------------

import re
from urllib.parse import urlparse

from .exceptions import InvalidEmail, InvalidURL


def email_validator(email: str) -> str | None:
    """
    Validates an email address.

    This function checks if the given email address is valid by matching it against a regular expression pattern. If the email address is not valid, an InvalidEmail exception is raised.

    Args:
        email (str): The email address to validate.

    Returns:
        str or None: The validated email address.

    Raises:
        InvalidEmail: Raised when the email address is not valid.

    Example:
        ```python
        email = "test@example.com"
        validated_email = email_validator(email)
        print(validated_email)
        ```
    """

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise InvalidEmail()
    return email


def url_validator(url: str) -> str | None:
    """
    Validates a URL.

    This function checks if the given URL is valid by parsing it using the `urlparse` function from the `urllib.parse` module. If the URL has both a scheme and a network location, it is considered valid and returned. Otherwise, an InvalidURL exception is raised.

    Args:
        url (str): The URL to validate.

    Returns:
        str or None: The validated URL.

    Raises:
        InvalidURL: Raised when the URL is not valid.

    Example:
        ```python
        url = "https://www.example.com"
        validated_url = url_validator(url)
        print(validated_url)
        ```
    """

    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
    except:
        raise InvalidURL()
