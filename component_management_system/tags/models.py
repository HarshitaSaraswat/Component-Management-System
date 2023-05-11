from database import Base, db, GUID


class Tag(Base):

    __tablename__ = "tags"
    label = db.Column(db.String(32), unique=True)
    metadata_id = db.Column(GUID(), db.ForeignKey("metadatas.id"), nullable=True)
