from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String

from component_management_system.database import Base


class Tag(Base):

    __tablename__: str = "tags"

    label: Column = Column(String(64), unique=True)

    def __repr__(self) -> str:
        return f'<Tag "{self.label}">'
