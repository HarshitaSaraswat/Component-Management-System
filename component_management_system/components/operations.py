from typing import Literal, Optional

from flask_sqlalchemy.query import Query

from ..files.models import File, FileType
from ..metadatas.models import Metadata
from ..metadatas.schemas import metadatas_schema
from ..tags.models import Tag
from ..utils import QueryPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE

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
		queried_list: list[dict[str, str]] = Metadata.elasticsearch(search_key.lower())
		paginated_query = QueryPagination(page=page, per_page=page_size, queried_list=queried_list)
		response = paginated_schema(metadatas_schema).dump(paginated_query)

		if columns == None:
			return response

		for data in response["items"]: # type: ignore
			to_pop = [key for key in data if key not in columns]
			for key in to_pop:
				data.pop(key)
		return response

	else:
		order_exp = eval(f"Metadata.{sort_by}.{sort_ord}()")
		query = query.order_by(order_exp)
		paginated_query = query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)

		return paginated_schema(metadatas_schema).dump(paginated_query)
