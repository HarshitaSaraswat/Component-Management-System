from flask import Flask

from .definations import db


def setup_db(app: Flask) -> None:
    from ..files import File
    from ..licenses import SPDX
    from ..metadatas import Metadata
    from ..tags import Tag

    db.init_app(app)
