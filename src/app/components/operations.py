from typing import Literal, Optional

from flask_sqlalchemy.query import Query

from ..files.models import File, FileType
from ..licenses.schemas import spdx_schema
from ..metadatas.models import Metadata
from ..metadatas.operations import read_files, read_tags
from ..tags.models import Tag
from ..utils import QueryPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE
from .schema import ComponentSchema


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
		response = paginated_schema(ComponentSchema).dump(paginated_query)


		for data in response.get("items"): # type: ignore
			metadata = Metadata.query.filter(Metadata.name==data.get("name")).one_or_none()
			data["files"] = read_files(metadata.id)
			data["license"] = spdx_schema.dump(metadata.license)
			data["tags"] = read_tags(metadata.id)
			data["id"] = metadata.id


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

		return paginated_schema(ComponentSchema).dump(paginated_query)


def create():...
