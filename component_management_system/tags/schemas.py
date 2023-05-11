from config import db, ma

from .models import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
