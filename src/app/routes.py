from flask import Flask, request

from ..authentication.utils import exchange_code_for_token


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

    @app.route("/login/github/authorized", methods=["GET"])
    def exchange_code():
        code = request.args.get("code")
        if not code:
            return "No code received", 400

        app.logger.debug(f"{code=}")
        auth_token = exchange_code_for_token(code)

        if auth_token is None:
            return "Could not authenticate with GitHub", 400

        app.logger.debug(f"{auth_token=}")

        return {
            "auth_token": auth_token,
        }, 200
