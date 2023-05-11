from database import GUID, Base, db

metadata_tag = db.Table(
    'metadata_tag',
    db.Column('metadata_id', GUID(), db.ForeignKey('metadatas.id')),
    db.Column('tag_id', GUID(), db.ForeignKey('tags.id')),
)


class Metadata(Base):

    __tablename__: str = "metadatas"
    components = db.relationship("Component", backref="metadata", cascade="all, delete, delete-orphan")
    tags = db.relationship("Tag", secondary=metadata_tag, backref="metadatas")
