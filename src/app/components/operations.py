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
from ..metadatas.schemas import MetadataSchema, metadata_schema
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

	print(columns)

	if columns:
		query = query.with_entities(*[eval(f"Metadata.{col}") for col in columns])

	if tags:
		query = query.filter(Metadata.tags.any(Tag.label.in_(tags)))

	query = query.filter(Metadata.files.any(File.type.in_(file_types)))

	if search_key:
		queried_list = [Metadata.query.filter(Metadata.name==md_name).one_or_none()
		  							for md_name in Metadata.elasticsearch(search_key.lower())]
		paginated_query = QueryPagination(page=page, per_page=page_size, queried_list=queried_list)
		components_resp = paginated_schema(ComponentSchema).dump(paginated_query) # type: ignore
		metadata_resp = paginated_schema(MetadataSchema).dump(paginated_query)


		for comp, metadata in zip(components_resp.get("items"), metadata_resp.get("items")): # type: ignore
			if columns is not None:
				to_pop = [key for key in metadata if key not in columns]
				for key in to_pop:
					metadata.pop(key)
			comp["metadata"] = metadata
			comp["id"] = metadata["id"]

		return components_resp

	else:
		order_exp = eval(f"Metadata.{sort_by}.{sort_ord}()")
		query = query.order_by(order_exp)
		paginated_query = query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)

		components_resp = paginated_schema(ComponentSchema).dump(paginated_query) # type: ignore
		metadata_resp = paginated_schema(MetadataSchema).dump(paginated_query)

		for comp, metadata in zip(components_resp.get("items"), metadata_resp.get("items")): # type: ignore
			comp["metadata"] = metadata
			comp["id"] = metadata["id"]
		return components_resp


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
