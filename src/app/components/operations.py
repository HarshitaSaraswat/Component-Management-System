
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

from typing import Literal, Optional

from flask_sqlalchemy.query import Query

from ..files.models import File, FileType
from ..files.operations import upload_to_github
from ..metadatas.models import Metadata
from ..metadatas.operations import _create as create_meatdata
from ..metadatas.operations import add_tags
from ..metadatas.schemas import metadata_schema, metadatas_schema
from ..tags.models import Tag
from ..utils import paginated_schema
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
	"""
	Reads components from the database based on the specified parameters.

	Parameters
	----------
	page : Optional[int], optional
		The page number for pagination. Defaults to None.
	page_size : Optional[int], optional
		The number of components per page. Defaults to None.
	search_key : Optional[str], optional
		The search key to filter components by name. Defaults to None.
	sort_by : Optional[str], optional
		The field to sort components by. Defaults to "name".
	sort_ord : Literal["desc"] | Literal["asc"], optional
		The sort order for the components. Defaults to "asc".
	file_types : list, optional
		The list of file types to filter components by. Defaults to [t.name for t in FileType].
	tags : Optional[list], optional
		The list of tags to filter components by. Defaults to None.
	columns : Optional[list], optional
		The list of columns to include in the query result. Defaults to None.

	Returns
	-------
	tuple
		A tuple containing the components response and the HTTP status code.

	Notes
	-----
	This function reads components from the database based on the specified parameters. It applies filters, sorting, and pagination to the query.
	"""

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

	components_resp = paginated_schema(ComponentSchema).dump(paginated_query)
	metadata_resp = metadatas_schema.dump(paginated_query)

	for component, metadata in zip(components_resp.get("items"), metadata_resp):
		component["metadata"] = metadata
		component["id"] = metadata["id"]
	return components_resp, 200


def create(component_data: dict):
	"""
	Creates a component based on the provided component data.

	Parameters
	----------
	component_data : dict
		The data for the component, including author, description, license_id, maintainer, name, version, and tags.

	Returns
	-------
	tuple
		A tuple containing the component response and the HTTP status code.

	Notes
	-----
	This function creates a component by creating metadata, adding tags, and uploading to GitHub. It returns the component response along with the HTTP status code.
	"""

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

	compo_response: dict = component_schema.dump(metadata)
	compo_response["metadata"] = metadata_schema.dump(metadata)

	return compo_response, 201
