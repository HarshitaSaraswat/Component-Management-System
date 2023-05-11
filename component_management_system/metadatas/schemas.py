from database import db, ma
from flask_sqlalchemy.session import Session
from sqlalchemy.orm.scoping import scoped_session

from .models import Metadata


class MetadataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metadata
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

metadata_schema = MetadataSchema()
metadatas_schema = MetadataSchema(many=True)
