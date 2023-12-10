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
from .models import File


class EnumToDictionary(fields.Field):
    """
    Custom field class for serializing an enumeration value to a dictionary.

    This class inherits from the `Field` class and overrides the `_serialize` method.
    The `_serialize` method takes a value, attribute, and object as arguments and returns a dictionary representation of the enumeration value.
    If the value is `None`, `None` is returned; otherwise, a dictionary with the name and value of the enumeration is returned.

    Args:
        value: The value to be serialized.
        attr: The attribute being serialized.
        obj: The object being serialized.

    Returns:
        dict[str, int] | None: A dictionary representation of the enumeration value, or `None` if the value is `None`.

    Example:
        ```python
        enum_field = EnumToDictionary()
        value = FileType.step
        result = enum_field._serialize(value, "file_type", None)
        print(result)
        ```
    """

    def _serialize(self, value, attr, obj, **kwargs) -> dict[str, int] | None:
        """
        Serializes an enumeration value to a dictionary.

        This method takes a value, attribute, and object as arguments and returns a dictionary representation of the enumeration value.
        If the value is `None`, `None` is returned; otherwise, a dictionary with the name and value of the enumeration is returned.

        Args:
            value: The value to be serialized.
            attr: The attribute being serialized.
            obj: The object being serialized.

        Returns:
            dict[str, int] | None: A dictionary representation of the enumeration value, or `None` if the value is `None`.
        """

        return None if value is None else {"name": value.name, "value": value.value}


class FileSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing File objects.

    This class inherits from `ma.SQLAlchemyAutoSchema` and defines the schema for the File model.
    It includes fields for the 'type' attribute, which is serialized using the `EnumToDictionary` class,
    and the 'metadata_id' attribute, which is treated as a string.
    The `Meta` class specifies the model, load_instance setting, and the SQLAlchemy session.

    Example:
        ```python
        schema = FileSchema()
        file_data = {"type": FileType.step, "metadata_id": "123"}
        result = schema.load(file_data)
        print(result)
        ```
    """

    type = EnumToDictionary(attribute=("type"))
    metadata_id = fields.String()

    class Meta:
        model = File
        load_instance = True
        sqla_session: scoped_session[Session] = db.session


file_schema = FileSchema()
files_schema = FileSchema(many=True)
