import re
from difflib import SequenceMatcher
from typing import Literal, Optional

from flask_sqlalchemy.query import Query
from sqlalchemy import or_

from ..files.models import File, FileType
from ..metadatas.models import Metadata
from ..metadatas.schemas import metadatas_schema
from ..tags.models import Tag
from ..utils import QueryPagination, paginated_schema


def _string_comparision(a: str, b: str):
	return SequenceMatcher(a=a, b=b).ratio()


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

	if columns:
		entities = set(columns)
		entities.add("name")
		query = query.with_entities(*[eval(f"Metadata.{col}") for col in entities])

	if tags:
		query = query.filter(Metadata.tags.any(Tag.label.in_(tags)))

	query = query.filter(Metadata.files.any(File.type.in_(file_types)))

	if search_key:
		search_key = search_key.lower()

		words = re.split(r" |,|\||-|_|\.", search_key)


		query = query.filter(or_(
			Metadata.name==search_key,
			Metadata.name.contains(search_key),
			Metadata.name.icontains(search_key),
			Metadata.name.like(search_key),
			Metadata.name.ilike(search_key),
			*(Metadata.name.contains(word) for word in words),
			*(Metadata.name.icontains(word) for word in words),
			*(Metadata.name.like(word) for word in words),
			*(Metadata.name.ilike(word) for word in words),
		))

		queried_list = sorted(query.all(), key=lambda x:_string_comparision(search_key, x.name), reverse=True)
		paginated_query = QueryPagination(page=page, per_page=page_size, max_per_page=50, queried_list=queried_list)

	else:
		order_exp = eval(f"Metadata.{sort_by}.{sort_ord}()")
		query = query.order_by(order_exp)
		paginated_query = query.paginate(page=page, per_page=page_size, max_per_page=50)

	return paginated_schema(metadatas_schema).dump(paginated_query)
