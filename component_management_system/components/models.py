from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy.sql.schema import Column

from ..database import Base, db
from ..database.guid import GUID


class ComponentType(Enum):
    step = 1
    fcform = 2

    @classmethod
    def serialize(cls, value) -> ComponentType:
        return eval(f"ComponentType.{value}")


class Component(Base):

    __tablename__: str = "components"

    url: Column = db.Column(db.String(2048),unique=True, nullable=False)
    type: Column = db.Column(db.Enum(ComponentType), nullable=False)
    metadata_id: Column = db.Column(GUID(), db.ForeignKey("metadatas.id"), nullable=True)

    __table_args__: tuple[Any] = (
        db.UniqueConstraint('metadata_id', 'type', name='_metadata_id_type_uc'),
    )

    def __repr__(self) -> str:
        return f'<Component "{self.url}", "{self.type}">'
