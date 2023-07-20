from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import Metadata


class MetadataSchema(ma.SQLAlchemyAutoSchema):
    license_id = fields.String()
    class Meta:
        model = Metadata
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

metadata_schema = MetadataSchema()
metadatas_schema = MetadataSchema(many=True)

Metadata.set_schemas(metadata_schema, metadatas_schema)
