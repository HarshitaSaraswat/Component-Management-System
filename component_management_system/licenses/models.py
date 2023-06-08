from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, String
from sqlalchemy.orm import validates
from ..database.validation import url_validator

from component_management_system.database import Base

from ..database.guid import GUID


class SPDX(Base):

    __tablename__: str = "spdx_licenses"

    fullname: Column = Column(String(200), unique=True)
    identifier: Column = Column(String(100), unique=True)
    license_page: Column = Column(String(150), unique=True)
    fsf_free: Column = Column(Boolean, default=False, nullable=False)
    osi_approved: Column = Column(Boolean, default=False, nullable=False)
    metadata_id = Column(GUID(), ForeignKey("metadatas.id"), nullable=True)


    @validates("license_page")
    def validate_license_page(self, key, url):
        return url_validator(url)


    def __repr__(self) -> str:
        return f'<SPDX "{self.fullname}">'
