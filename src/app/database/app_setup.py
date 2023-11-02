from flask import Flask

from .definations import db


def setup_db(app: Flask) -> None:
	from ..files.models import File
	from ..licenses.models import SPDX
	from ..metadatas.models import Metadata
	from ..tags.models import Tag

	db.init_app(app)
