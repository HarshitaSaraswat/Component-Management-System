import requests

from ..config import Config


def exchange_code_for_token(code: str):
    if not code:
        raise ValueError("The authentication code has to be supplied!")

    if Config.GITHUB_OAUTH_CLIENT_ID is None:
        raise ValueError("The GitHub OAuth Client ID has to be supplied!")

    if Config.GITHUB_OAUTH_CLIENT_SECRET is None:
        raise ValueError("The GitHub OAuth Client Secret has to be supplied!")

    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": Config.GITHUB_OAUTH_CLIENT_ID,
            "client_secret": Config.GITHUB_OAUTH_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
        timeout=10,
    )

    if response.status_code == 200:
        return response.json().get("access_token")

    def get_user(auth_token: str):
        if not auth_token:
            raise ValueError("The authentication token has to be supplied!")

        response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {auth_token}"},
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()
