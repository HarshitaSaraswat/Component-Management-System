from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy.types import String, Integer
from sqlalchemy.types import Enum as dbEnum
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import validates

from ..database import Base
from ..database.guid import GUID
from ..database.validation import url_validator


class ComponentType(Enum):
    step = 1
    fcstd = 2

    @classmethod
    def serialize(cls, value) -> ComponentType:
        return eval(f"ComponentType.{value}")


class Component(Base):

    __tablename__: str = "components"

    url = Column(String(2048),unique=True, nullable=False)
    type = Column(dbEnum(ComponentType), nullable=False)
    size = Column(Integer, nullable=False)
    metadata_id = Column(GUID(), ForeignKey("metadatas.id"), nullable=True)

    __table_args__: tuple[Any] = (
        UniqueConstraint('metadata_id', 'type', name='_metadata_id_type_uc'),
    )

    def __repr__(self) -> str:
        return f'<Component "{self.url}", "{self.type}">'

    @validates("thumbnail")
    def validate_thumbnail(self, key, url):
        return url_validator(url)
