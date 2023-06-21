from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import File


class EnumToDictionary(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs) -> dict[str, int] | None:
        if value is None:
            return None
        return {"name": value.name, "value": value.value}


class FileSchema(ma.SQLAlchemyAutoSchema):
    type = EnumToDictionary(attribute=("type"))
    metadata_id = fields.String()
    class Meta:
        model = File
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

file_schema = FileSchema()
files_schema = FileSchema(many=True)
