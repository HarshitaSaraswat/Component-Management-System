import pathlib

import connexion
from connexion import FlaskApp
from flask import Flask

from .database import db

basedir: pathlib.Path = pathlib.Path(__file__).parent.resolve()


def create_app(host="0.0.0.0", port=8000, debug=True) -> FlaskApp:

	connex_app: FlaskApp = connexion.FlaskApp(__name__, specification_dir=basedir)
	connex_app.add_api(basedir / "swagger.yml")
	connex_app.host = host
	connex_app.port = port
	connex_app.debug = debug

	app: Flask = connex_app.app # type: ignore

	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'component_management.db'}"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	from .components.models import Component
	from .licenses.models import SPDX
	from .metadatas.models import Metadata
	from .tags.models import Tag

	db.init_app(app)

	return connex_app


def production_app(host, port) -> FlaskApp:
    app: FlaskApp = create_app(host, port, False)
    # TODO make production config
    return app
