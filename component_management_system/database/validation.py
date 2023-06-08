

class InvalidEmail(Exception):...
class InvalidURL(Exception):...


def email_validator(email: str) -> str: #TODO complete email validation
    if '@' not in email:
        raise InvalidEmail()
    return email

def url_validator(url: str) -> str: #TODO complete url validation
    if "www." not in url:
        raise InvalidURL()
    return url
