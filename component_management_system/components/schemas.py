from config import db, ma

from component_management_system.components.models import Component


class ComponentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Component
        load_instance = True
        sqla_session = db.session
