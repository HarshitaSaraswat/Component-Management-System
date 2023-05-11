from enum import Enum

from database import GUID, Base, db


class ComponentType(Enum):
    step = 1
    fcform = 2

    @classmethod
    def serialize(cls, value):
        return eval(f"ComponentType.{value}")


class Component(Base):

    __tablename__ = "components"

    url = db.Column(db.String(2048),unique=True, nullable=False)
    type = db.Column(db.Enum(ComponentType), nullable=False)
    metadata_id = db.Column(GUID(), db.ForeignKey("metadatas.id"), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('metadata_id', 'type', name='_metadata_id_type_uc'),
    )

    def __repr__(self):
        return f'<Component "{self.url}", "{self.type}">'
