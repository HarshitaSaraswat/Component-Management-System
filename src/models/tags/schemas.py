# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
# |																|
# |             Copyright 2023 - 2023, Amulya Paritosh			|
# |																|
# |  This file is part of Component Library Plugin for FreeCAD.	|
# |																|
# |               This file was created as a part of				|
# |              Google Summer Of Code Program - 2023			|
# |																|
# --------------------------------------------------------------

from flask_sqlalchemy.session import Session
from marshmallow import fields
from sqlalchemy.orm.scoping import scoped_session

from ...database import db, ma
from .models import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Tag objects.

    Attributes:
        metadata_id (str): The ID of the metadata.

    Example:
        ```python
        tag_schema = TagSchema()
        ```
    """

    metadata_id = fields.String()

    class Meta:
        model = Tag
        load_instance = True
        sqla_session: scoped_session[Session] = db.session


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
