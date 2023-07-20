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
