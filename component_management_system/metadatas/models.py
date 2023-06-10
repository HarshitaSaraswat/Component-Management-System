from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Relationship, relationship, validates
from sqlalchemy.types import Float, String

from ..database import Base, db
from ..database.guid import GUID
from ..database.validation import email_validator, url_validator

metadata_tag = db.Table(
    'metadata_tag',
    Column('metadata_id', GUID(), ForeignKey('metadatas.id')),
    Column('tag_id', GUID(), ForeignKey('tags.id')),
)


class InvalidRating(Exception):...


class Metadata(Base):

    __tablename__: str = "metadatas"
    __allow_unmapped__ = True

    name = Column(String(200), nullable=False)
    version = Column(String(50), nullable=False)
    maintainer = Column(String(100), nullable=False)

    author = Column(String(100))
    thumbnail = Column(String(200), unique=True)
    description = Column(String(500))
    rating = Column(Float)

    license_id = Column(GUID(), ForeignKey("spdx_licenses.id"), nullable=True)
    components: Relationship = relationship("Component", backref="metadata", cascade="all, delete, delete-orphan") # type: ignore
    tags: Relationship = relationship("Tag", secondary=metadata_tag, backref="metadatas") # type: ignore


    @validates("maintainer")
    def validate_maintainer(self, key, email):
        return email_validator(email)

    @validates("author")
    def validate_author(self, key, email):
        return email_validator(email)

    @validates("thumbnail")
    def validate_thumbnail(self, key, url):
        return url_validator(url)

    @validates("rating")
    def validate_rating(self, key, rating):
        if rating > 5:
            raise InvalidRating()
        return rating

    def __repr__(self) -> str:
        return f'<Metadata "{self.name}">'
