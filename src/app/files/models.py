
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
    step = 1
    fcstd = 2
    fcstd1 = 3
    stl = 4
    stp = 5

    @classmethod
    def serialize(cls, value) -> FileType:
        return eval(f"FileType.{value}")


class File(Base):

    __tablename__: str = "files"

    url = Column(String(2048),unique=True, nullable=False)
    type = Column(dbEnum(FileType), nullable=False)
    size = Column(Integer, nullable=False)

    metadata_id = Column(GUID(), ForeignKey("metadatas.id"), nullable=False)


    def __repr__(self) -> str:
        return f'<File "{self.url}", "{self.type}">'

    @validates("thumbnail")
    def validate_thumbnail(self, key, url):
        return url_validator(url)
