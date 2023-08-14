from copy import copy
from typing import Literal, Optional

from flask_sqlalchemy.query import Query

from ..files.models import File, FileType
from ..files.operations import upload_to_github
from ..licenses.schemas import spdx_schema
from ..metadatas.models import Metadata
from ..metadatas.operations import add_tags
from ..metadatas.operations import _create as create_meatdata
from ..metadatas.operations import read_files, read_tags
from ..metadatas.schemas import MetadataSchema, metadata_schema, metadatas_schema
from ..tags.models import Tag
from ..utils import QueryPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE
from .schema import ComponentSchema, component_schema


def read(
	page: Optional[int] = None,
	page_size: Optional[int] = None,
	search_key: Optional[str] = None,
	sort_by: Optional[str] = "name",
	sort_ord: Literal["desc"] | Literal["asc"] = "asc",
	file_types: list = [t.name for t in FileType],
	tags: Optional[list] = None,
	columns: Optional[list] = None,
):

	query: Query = Metadata.query

	if tags:
		query = query.filter(Metadata.tags.any(Tag.label.in_(tags)))

	query = query.filter(Metadata.files.any(File.type.in_(file_types)))

	if search_key:
		query = query.filter(Metadata.name.in_(Metadata.elasticsearch(search_key.lower())))

	if columns:
		query = query.with_entities(*[eval(f"Metadata.{col}") for col in columns])

	order_exp = eval(f"Metadata.{sort_by}.{sort_ord}()")
	query = query.order_by(order_exp)
	paginated_query = query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)

	components_resp = paginated_schema(ComponentSchema).dump(paginated_query) # type: ignore
	metadata_resp = metadatas_schema.dump(paginated_query)

	for component, metadata in zip(components_resp.get("items"), metadata_resp): # type: ignore
		component["metadata"] = metadata
		component["id"] = metadata["id"]
	return components_resp, 200


def create(component_data: dict):
	metadata_data: dict = {
		"author": component_data.get("author", ""),
		"description": component_data.get("description", ""),
		"license_id": component_data.get("license_id", ""),
		"maintainer": component_data.get("maintainer", ""),
		"name": component_data.get("name", ""),
		"rating": 0,
		"version": component_data.get("version", ""),
	}

	metadata: Metadata = create_meatdata(metadata_data)
	add_tags(metadata.id, component_data.get("tags"))
	component_data["metadata_id"] = str(metadata.id)
	upload_to_github(component_data)

	compo_response: dict = component_schema.dump(metadata) # type: ignore
	compo_response["metadata"] = metadata_schema.dump(metadata)

	return compo_response, 201
