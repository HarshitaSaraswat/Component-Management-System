from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Relationship, relationship, validates
from sqlalchemy.types import Float, String

from ..database import ElasticSearchBase, db
from ..database.guid import GUID
from ..database.validation import email_validator, url_validator
from ..files.models import File
from ...config import Config
metadata_tag = db.Table(
    'metadata_tag',
    Column('metadata_id', GUID(), ForeignKey('metadatas.id')),
    Column('tag_id', GUID(), ForeignKey('tags.id')),
)


class InvalidRating(Exception):...


class Metadata(ElasticSearchBase):

    __tablename__: str = "metadatas"
    __allow_unmapped__ = True

    name = Column(String(200), nullable=False, unique=True)
    version = Column(String(50), nullable=False)
    maintainer = Column(String(100), nullable=False)

    author = Column(String(100))
    thumbnail = Column(String(200), unique=True)
    description = Column(String(500))
    rating = Column(Float)

    license_id = Column(GUID(), ForeignKey("spdx_licenses.id"), nullable=True)

    files: Relationship = relationship("File", backref="metadata", cascade="all, delete, delete-orphan") # type: ignore
    tags: Relationship = relationship("Tag", secondary=metadata_tag, backref="metadatas") # type: ignore


    @validates("maintainer")
    def validate_maintainer(self, key, email):
# sourcery skip: swap-if-expression
        return email_validator(email) if not Config.DEBUG else email

    @validates("author")
    def validate_author(self, key, author):
# sourcery skip: swap-if-expression
        return email_validator(author) if not Config.DEBUG else author

    @validates("thumbnail")
    def validate_thumbnail(self, key, url):
# sourcery skip: swap-if-expression
        return url_validator(url) if not Config.DEBUG else url

    @validates("rating")
    def validate_rating(self, key, rating):
        if rating > 5:
            raise InvalidRating()
        return rating

    def add_tag(self, tag):
        self.tags.append(tag)
        self.commit()

    def add_file(self, file):
        self.files.append(file)
        self.commit()

    def delete(self):
        return super().delete("name", self.name)

    def update(self):
        return super().update("name", self.name)

    def __repr__(self) -> str:
        return f'<Metadata "{self.name}">'
