from sqlalchemy import Column
from ..database import Base, db
from ..database.guid import GUID

metadata_tag = db.Table(
    'metadata_tag',
    db.Column('metadata_id', GUID(), db.ForeignKey('metadatas.id')),
    db.Column('tag_id', GUID(), db.ForeignKey('tags.id')),
)


class Metadata(Base):

    __tablename__: str = "metadatas"

    name:Column = db.Column(db.String(200), nullable=False)
    size: Column = db.Column(db.Integer, nullable=False)
    version:Column = db.Column(db.String(50), nullable=False)
    maintainer:Column = db.Column(db.String(100), nullable=False) #TODO make it a email column Type

    author: Column = db.Column(db.String(100)) #TODO make it a email column Type
    thumbnail: Column = db.Column(db.String(200), unique=True)
    description: Column = db.Column(db.String(500)) #TODO make it url column type
    rating: Column = db.Column(db.Float)

    license:Column = db.Column(db.String(100)) #TODO make it a relationship
    components = db.relationship("Component", backref="metadata", cascade="all, delete, delete-orphan")
    tags = db.relationship("Tag", secondary=metadata_tag, backref="metadatas")
