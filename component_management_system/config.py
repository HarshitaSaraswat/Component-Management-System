import pathlib

import connexion
import database
from connexion import FlaskApp
from flask.app import Flask

basedir: pathlib.Path = pathlib.Path(__file__).parent.resolve()
connex_app: FlaskApp = connexion.App(__name__, specification_dir=basedir)

app: Flask = connex_app.app # type: ignore
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'component_management.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from components.models import Component
from metadatas.models import Metadata
from tags.models import Tag

database.db.init_app(app)


with app.app_context():
	database.db.create_all()
