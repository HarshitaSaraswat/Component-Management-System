import uuid

from config import db
from sqlalchemy.dialects.postgresql import UUID

class Tag(db.Model):

    __tablename__ = "tags"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(32), unique=True)
    metadata_id = db.Column(db.Integer, db.ForeignKey("metadatas.id"), nullable=False)
