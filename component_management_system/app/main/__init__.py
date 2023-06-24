from os import path

import connexion
from connexion import FlaskApp
from flask import Flask

from ...config import Config, basedir
from ..database import db

# basedir: pathlib.Path = pathlib.Path(__file__).parent.resolve()


def create_app(config_class=Config) -> Flask:

	connex_app: FlaskApp = connexion.FlaskApp(__name__, specification_dir=basedir)
	connex_app.add_api(path.join(basedir,"app/main/swagger.yml"))

	app: Flask = connex_app.app # type: ignore
	app.config.from_object(config_class)

	from ..files.models import File
	from ..licenses.models import SPDX
	from ..metadatas.models import Metadata
	from ..tags.models import Tag

	db.init_app(app)

	return app
