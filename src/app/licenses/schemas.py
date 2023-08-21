
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

from flask_sqlalchemy.session import Session
from sqlalchemy.orm.scoping import scoped_session

from ..database import db, ma
from .models import SPDX


class SPDXSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing SPDX licenses.

    This class inherits from `ma.SQLAlchemyAutoSchema` and defines the schema for the SPDX model.
    The `Meta` class specifies the model, load_instance setting, and the SQLAlchemy session.

    Example:
        ```python
        schema = SPDXSchema()
        license_data = {"fullname": "MIT License", "identifier": "MIT", "license_page": "https://opensource.org/licenses/MIT"}
        result = schema.load(license_data)
        print(result)
        ```
    """
    class Meta:
        model = SPDX
        load_instance = True
        sqla_session: scoped_session[Session] = db.session

spdx_schema = SPDXSchema()
spdxs_schema = SPDXSchema(many=True)
