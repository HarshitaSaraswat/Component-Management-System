from config import db, ma

from .models import Metadata


class MetadataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metadata
        load_instance = True
        sqla_session = db.session
