from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

from ...database import Base
from ...database.guid import GUID


class Attribute(Base):
    """
    Represents metadata for a component.

    This class inherits from `ElasticSearchBase` and defines the metadata fields for a component.
    The class includes columns for name, version, maintainer, author, thumbnail, description, rating, and license ID.
    It also defines relationships with files and tags.

    The class provides methods for adding tags and files, as well as deleting and updating the metadata.

    Example:
        ```python
        metadata = Metadata()
        metadata.name = "Component A"
        metadata.version = "1.0.0"
        metadata.maintainer = "John Doe"
        metadata.add_tag("tag1")
        metadata.add_file("file1")
        metadata.commit()
        print(metadata)
        ```
    """

    __tablename__: str = "attributes"
    __allow_unmapped__ = True

    key = Column(String(50), nullable=False)
    value = Column(String(200))

    metadata_id = Column(GUID(), ForeignKey("metadatas.id"), nullable=False)
