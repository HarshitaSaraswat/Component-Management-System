from sqlalchemy.sql.schema import Column

from component_management_system.database import Base, db


class SPDX(Base):

    __tablename__: str = "spdx_licenses"

    fullname: Column = db.Column(db.String(200), unique=True)
    identifier: Column = db.Column(db.String(100), unique=True)
    url: Column = db.Column(db.String(150), unique=True)
    fsf_free: Column = db.Column(db.Boolean, default=False, nullable=False)
    osi_approved: Column = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self) -> str:
        return f'<SPDX "{self.fullname}">'
