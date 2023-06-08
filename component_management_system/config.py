import pathlib

import connexion
from connexion import FlaskApp
from flask.app import Flask

from .database import db

basedir: pathlib.Path = pathlib.Path(__file__).parent.resolve()
connex_app: FlaskApp = connexion.App(__name__, specification_dir=basedir)

app: Flask = connex_app.app # type: ignore
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'component_management.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from .components.models import Component
from .licenses.models import SPDX
from .metadatas.models import Metadata
from .tags.models import Tag

db.init_app(app)


with app.app_context():
	db.create_all()
	# from .licenses.db_entry import make_db_entry
	# make_db_entry()
