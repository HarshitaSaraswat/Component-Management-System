
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

from __future__ import annotations

from enum import Enum

from sqlalchemy.orm import validates
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Enum as dbEnum
from sqlalchemy.types import Integer, String

from ..database import Base
from ..database.guid import GUID
from ..database.validation import url_validator


class FileType(Enum):
    """
    Enumeration class representing different file types.

    This class defines different file types as enumeration members. Each member has an associated integer value.
    The `serialize` class method can be used to convert a string value to the corresponding `FileType` enumeration member.

    Example:
        ```python
        value = "step"
        file_type = FileType.serialize(value)
        print(file_type)
        ```
    """

    step = 1
    fcstd = 2
    fcstd1 = 3
    stl = 4
    stp = 5

    @classmethod
    def serialize(cls, value) -> FileType:
        """
        Converts a string value to the corresponding `FileType` enumeration member.

        This class method takes a string value and evaluates it as an attribute of the `FileType` enumeration.
        The evaluated attribute is returned as the corresponding `FileType` enumeration member.

        Args:
            value (str): The string value to be serialized.

        Returns:
            FileType: The corresponding `FileType` enumeration member.

        Example:
            ```python
            value = "step"
            file_type = FileType.serialize(value)
            print(file_type)
            ```
        """

        return eval(f"FileType.{value}")


class File(Base):
    """
    Represents a file in the database.

    This class inherits from the `Base` class and defines the structure of the `files` table in the database.
    It includes columns for the URL, type, size, and metadata ID of the file.
    The `__repr__` method returns a string representation of the file.
    The `validate_thumbnail` method is a validator for the `thumbnail` column.

    Attributes:
        __tablename__ (str): The name of the table in the database.

    Example:
        ```python
        file = File(url="https://example.com/file.txt", type=FileType.step, size=1024, metadata_id=1)
        print(file)
        ```
    """

    __tablename__: str = "files"

    url = Column(String(2048),unique=True, nullable=False)
    type = Column(dbEnum(FileType), nullable=False)
    size = Column(Integer, nullable=False)

    metadata_id = Column(GUID(), ForeignKey("metadatas.id"), nullable=False)


    def __repr__(self) -> str:
        return f'<File "{self.url}", "{self.type}">'

    @validates("thumbnail")
    def validate_thumbnail(self, key, url):
        """
    Validator for the 'thumbnail' column of the File class.

    This validator method takes the key and URL as arguments and applies the 'url_validator' function to validate the URL.

    Args:
        key (str): The key of the column being validated.
        url (str): The URL to be validated.

    Returns:
        str: The validated URL.

    Example:
        ```python
        file = File()
        validated_url = file.validate_thumbnail("thumbnail", "https://example.com/image.jpg")
        print(validated_url)
        ```
    """

        return url_validator(url)
