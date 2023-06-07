from typing import Any

from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import Component


class EnumToDictionary(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs) -> dict[str, int] | None:
        if value is None:
            return None
        return {"name": value.name, "value": value.value}


class ComponentSchema(ma.SQLAlchemyAutoSchema):
    type = EnumToDictionary(attribute=("type"))
    metadata_id = fields.String()
    class Meta:
        model = Component
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)
