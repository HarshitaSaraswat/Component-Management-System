from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    metadata_id = fields.String()
    class Meta:
        model = Tag
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
