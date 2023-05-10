import uuid
from enum import Enum

from config import db
from sqlalchemy.dialects.postgresql import UUID


class ComponentType(Enum):
    step = 1
    fcform = 2


class Component(db.Model):

    __tablename__ = "components"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = db.Column(db.String(2048), unique=True, nullable=False)
    type = db.Column(db.Enum(ComponentType), nullable=False)
    metadata_id = db.Column(db.Integer, db.ForeignKey("metadatas.id"), nullable=False)
