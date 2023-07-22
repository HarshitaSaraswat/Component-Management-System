from typing import Literal, Optional

from flask_sqlalchemy.query import Query
from copy import copy
from ..files.models import File, FileType
from ..files.operations import create as create_file
from ..files.schemas import file_schema
from ..licenses.schemas import spdx_schema
from ..metadatas.models import Metadata
from ..metadatas.operations import create as create_meatdata
from ..metadatas.operations import read_files, read_tags, add_tags, add_file
from ..metadatas.schemas import MetadataSchema
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
		queried_list: list[Metadata] = Metadata.elasticsearch(search_key.lower())
		paginated_query = QueryPagination(page=page, per_page=page_size, queried_list=queried_list)
		response = paginated_schema(MetadataSchema).dump(paginated_query)


		for data in response.get("items"): # type: ignore
			temp_data = copy(data)
			metadata = Metadata.query.filter(Metadata.name==temp_data.get("name")).one_or_none()
			temp_data["id"] = metadata.id
			data.clear()
			data["id"] = metadata.id
			data["metadata"] = temp_data
			data["files"] = read_files(metadata.id)
			data["license"] = spdx_schema.dump(metadata.license)
			data["tags"] = read_tags(metadata.id)


		if columns != None:
			for data in response["items"]: # type: ignore
				to_pop = [key for key in data if key not in columns]
				for key in to_pop:
					data.pop(key)

		return response

	else:
		order_exp = eval(f"Metadata.{sort_by}.{sort_ord}()")
		query = query.order_by(order_exp)
		paginated_query = query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)

		components_resp = paginated_schema(ComponentSchema).dump(paginated_query)
		metadata_resp = paginated_schema(MetadataSchema).dump(paginated_query)

		for comp, metadata in zip(components_resp.get("items"), metadata_resp.get("items")):
			comp["metadata"] = metadata
			comp["id"] = metadata["id"]
		return components_resp

def create(component_data):
	print(component_data)
	metadata_data: dict = component_data.get("metadata")
	file_data: dict = component_data.get("file")
	tags: list[str] = component_data.get("tags")

	metadata, _ = create_meatdata(metadata_data)
	add_tags(metadata["id"], tags)
	file, _ = create_file(metadata["id"], file_data)
	add_file(metadata["id"], file["id"])

	return metadata, 201
