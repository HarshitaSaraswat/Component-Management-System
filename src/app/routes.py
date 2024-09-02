from flask import Flask, request

<<<<<<< HEAD
from src.log import logger

from ..authentication.utils import (
    encode_auth_token,
    exchange_code_for_token,
    get_github_user,
)
from ..models.users import User
=======
from .authentication import exchange_code_for_token
>>>>>>> cec9cd2 (Update dependencies and add logging and authentication routes)


def create_routes(app: Flask):
    @app.route("/")
    def root_route():
        app.logger.debug("A debug message")
        app.logger.info("An info message")
        app.logger.warning("A warning message")
        app.logger.error("An error message")
        app.logger.critical("A critical message")

        return "Hello, World!"

    @app.route("/api", methods=["GET"])
    def api():
        return "Component Management System API", 200

<<<<<<< HEAD
    @app.route("/login/app/authorize", methods=["GET"])
    def auth_with_access_token():  # -> tuple[Literal['No access token received'], Literal[400]] ...:
        access_token = request.headers.get("access_token")
        if not access_token:
            return "No access token received", 400

    #     user_data = get_github_user(access_token)
    #     user = User.query.filter_by(username=user_data["login"]).first()

    #     if not user:
    #         user = User(username=user_data["login"], admin=False)
    #         user.create()
    #     jwt = encode_auth_token(str(user.id))
    #     logger.debug(f"{jwt=}")
    #     return {
    #         "jwt": jwt,
    #     }, 200

=======
>>>>>>> cec9cd2 (Update dependencies and add logging and authentication routes)
    @app.route("/login/github/authorized", methods=["GET"])
    def exchange_code():
        code = request.args.get("code")
        if not code:
            return "No code received", 400

<<<<<<< HEAD
=======
        app.logger.debug(f"{code=}")
>>>>>>> cec9cd2 (Update dependencies and add logging and authentication routes)
        auth_token = exchange_code_for_token(code)

    #     if auth_token is None:
    #         return "Could not authenticate with GitHub", 400

<<<<<<< HEAD
        user_data = get_github_user(auth_token)
        user = User.query.filter_by(username=user_data["login"]).first()

    #     if not user:
    #         user = User(username=user_data["login"], admin=False)
    #         user.create()

        return {
            "github_auth_token": auth_token,
            "jwt": encode_auth_token(user.id),
=======
        app.logger.debug(f"{auth_token=}")

        return {
            "auth_token": auth_token,
>>>>>>> cec9cd2 (Update dependencies and add logging and authentication routes)
        }, 200
