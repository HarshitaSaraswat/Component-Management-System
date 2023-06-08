from sqlalchemy.sql.schema import Column

from component_management_system.database import Base, db


class Tag(Base):

    __tablename__: str = "tags"

    label: Column = db.Column(db.String(32), unique=True)

    def __repr__(self) -> str:
        return f'<Tag "{self.label}">'
