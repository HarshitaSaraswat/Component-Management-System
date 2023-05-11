from database import db, ma
from marshmallow import fields

from .models import Component


class EnumToDictionary(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"name": value.name, "value": value.value}


class ComponentSchema(ma.SQLAlchemyAutoSchema):
    type = EnumToDictionary(attribute=("type"))
    metadata_id = fields.String()
    class Meta:
        model = Component
        load_instance = True
        sqla_session = db.session

component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)
