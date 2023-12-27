import re

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

from ...database import ElasticSearchBase
from ...database.guid import GUID
from ...database.utils import make_fuzzy_query


class Attribute(ElasticSearchBase):
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

    @classmethod
    def elasticsearch(cls, search_key: str) -> set[str]:
        """
        Performs an Elasticsearch search based on the specified search key and returns a set of matching names.

        Args:
            search_key: The key to search for.

        Returns:
            set[str]: A set of matching names.
        """
        value_list = re.split(r" |,|\||-|_|\.", search_key)
        query = {
            "bool": {
                "must": [make_fuzzy_query(value) for value in value_list],
                # "should": query_list,
            }
        }

        response = super().elasticsearch(cls.__tablename__, query)
        # return {hit["_source"]["metadata_id"] for hit in response["hits"]["hits"]}
        return response
