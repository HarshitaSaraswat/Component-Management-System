import pathlib

import connexion
import database

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'component_management.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from components.models import Component
from metadatas.models import Metadata
from tags.models import Tag

database.db.init_app(app) # init of db is deferred


with app.app_context():
	database.db.create_all()
#     print("creating db...")
#     db.create_all()
#     db.session.commit()
