from config import db, ma

from .models import Component


class ComponentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Component
        load_instance = True
        sqla_session = db.session
