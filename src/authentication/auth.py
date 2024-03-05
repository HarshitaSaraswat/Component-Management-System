from ..models.users import User
from .utils import encode_auth_token, exchange_code_for_token, get_user


def sign_up(code):
    """
    Sign up a new user.
    """
    auth_token = exchange_code_for_token(code)
    user_data = get_user(auth_token)
    user = User.query.filter_by(username=user_data["login"]).first()

    if not user:
        user = User(username=user_data["login"])
        user.save()

    jwt = encode_auth_token(user.id)
    return auth_token, jwt


def login(github_token):
    """
    Login a user.
    """
    user_data = get_user(github_token)
    user = User.query.filter_by(username=user_data["login"]).first()
    return encode_auth_token(user.id)
