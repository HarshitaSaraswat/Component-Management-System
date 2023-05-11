from database import db, ma
from marshmallow import fields

from .models import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    metadata_id = fields.String()
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
