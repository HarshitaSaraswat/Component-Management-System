import uuid

from config import db
from sqlalchemy.dialects.postgresql import UUID


class Metadata(db.Model):

    __tablename__ = "metadatas"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    components = db.relationship("Component", backref="metadata", cascade="all, delete, delete-orphan")
    tags = db.relationship("Tag", backref="metadata")
