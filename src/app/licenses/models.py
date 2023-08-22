
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

from sqlalchemy.orm import Relationship, relationship, validates
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Boolean, String

from ..database import Base
from ..database.validation import url_validator


class SPDX(Base):
    """
    Represents an SPDX license in the database.

    This class inherits from the `Base` class and defines the structure of the `spdx_licenses` table in the database.
    It includes columns for the fullname, identifier, license_page, fsf_free, and osi_approved attributes of the SPDX license.
    The `metadatas` relationship defines the relationship between SPDX licenses and metadata.
    The `validate_license_page` method is a validator for the `license_page` column.
    The `__repr__` method returns a string representation of the SPDX license.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __allow_unmapped__ (bool): Flag indicating whether unmapped attributes are allowed.

    Example:
        ```python
        license = SPDX(fullname="MIT License", identifier="MIT", license_page="https://opensource.org/licenses/MIT")
        print(license)
        ```
    """

    __tablename__: str = "spdx_licenses"
    __allow_unmapped__ = True

    fullname: Column = Column(String(200), unique=True)
    identifier: Column = Column(String(100), unique=True)
    license_page: Column = Column(String(150), unique=True)
    fsf_free: Column = Column(Boolean, default=False, nullable=False)
    osi_approved: Column = Column(Boolean, default=False, nullable=False)

    metadatas: Relationship = relationship("Metadata", backref="license")


    @validates("license_page")
    def validate_license_page(self, key, url):
        """
        Validator for the 'license_page' column of the SPDX class.

        This validator method takes the key and URL as arguments and applies the 'url_validator' function to validate the URL.

        Args:
            key (str): The key of the column being validated.
            url (str): The URL to be validated.

        Returns:
            str: The validated URL.

        Example:
            ```python
            spdx = SPDX()
            validated_url = spdx.validate_license_page("license_page", "https://opensource.org/licenses/MIT")
            print(validated_url)
            ```
        """

        return url_validator(url)


    def __repr__(self) -> str:
        return f'<SPDX "{self.fullname}">'
