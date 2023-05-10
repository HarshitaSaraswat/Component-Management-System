from config import db, ma

from component_management_system.tags.models import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session
