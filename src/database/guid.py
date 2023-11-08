
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

import uuid
from typing import Any

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR, TypeDecorator, TypeEngine


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(32), storing as stringified hex values.

    Methods:
        load_dialect_impl(dialect): Returns the appropriate type engine based on the dialect.
        process_bind_param(value, dialect): Processes the value before binding it as a parameter.
        process_result_value(value, dialect): Processes the value after retrieving it from the database.

    Returns:
        The appropriate type engine or processed value based on the method called.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect) -> TypeEngine[UUID] | TypeEngine[str]:
        """
        Returns the appropriate type engine based on the dialect.

        Args:
            dialect: The dialect to check.

        Returns:
            TypeEngine[UUID] or TypeEngine[str]: The appropriate type engine based on the dialect.
        """

        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect) -> Any | str | None:
        """
        Processes the value before binding it as a parameter based on the dialect.

        Args:
            value: The value to process.
            dialect: The dialect to check.

        Returns:
            Any, str, or None: The processed value.
        """

        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect) -> Any | UUID | None:
        """
        Processes the value after retrieving it from the database based on the dialect.

        Args:
            value: The value to process.
            dialect: The dialect to check.

        Returns:
            Any, UUID, or None: The processed value.
        """

        if value is not None and not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value
