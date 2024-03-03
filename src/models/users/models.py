from sqlalchemy.orm import Relationship, relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Boolean, String

from ...database import Base


class User(Base):

    __tablename__: str = "users"
    __allow_unmapped__ = True

    username: Column = Column(String(64), unique=True)
    metadatas: Relationship = relationship("Metadata", backref="user")
    admin: Column = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'<User "{self.username}">'
