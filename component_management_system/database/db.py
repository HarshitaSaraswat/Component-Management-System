import uuid

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .guid import GUID

db = SQLAlchemy()
ma = Marshmallow()

class Base(db.Model):

    __abstract__ = True

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,
                    default=db.func.current_timestamp(),
                    onupdate=db.func.current_timestamp())
