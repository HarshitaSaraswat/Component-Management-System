from database import Base, db


class Metadata(Base):

    __tablename__ = "metadatas"
    components = db.relationship("Component", backref="metadata", cascade="all, delete, delete-orphan")
    tags = db.relationship("Tag", backref="metadata")
