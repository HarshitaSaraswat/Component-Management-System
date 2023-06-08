from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import SPDX


class SPDXSchema(ma.SQLAlchemyAutoSchema):
    metadata_id = fields.String()
    class Meta:
        model = SPDX
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

spdx_schema = SPDXSchema()
spdxs_schema = SPDXSchema(many=True)
