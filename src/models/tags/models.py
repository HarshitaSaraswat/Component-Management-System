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

from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String

from ...database import Base


class Tag(Base):
    """
    Represents a Tag object.

    Attributes:
        __tablename__ (str): The name of the database table.
        label (Column): The label of the tag.

    Methods:
        __repr__(): Returns a string representation of the Tag object.

    """

    __tablename__: str = "tags"

    label: Column = Column(String(64), unique=True)

    def __repr__(self) -> str:
        return f'<Tag "{self.label}">'
