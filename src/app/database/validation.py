
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

import re
from urllib.parse import urlparse


class InvalidEmail(Exception):...
class InvalidURL(Exception):...


def email_validator(email: str) -> str | None:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise InvalidEmail()
    return email

def url_validator(url: str) -> str | None:
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
    except:
        raise InvalidURL()
