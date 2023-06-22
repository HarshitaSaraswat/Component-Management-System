from dataclasses import dataclass
import typing as t

from flask_sqlalchemy.query import Query
from flask_sqlalchemy.pagination import QueryPagination as BaseQueryPagination
from marshmallow import Schema, fields


@dataclass()
class PsudoPagination:
	page: int
	per_page: int | None
	items: list
	total: int


class QueryPagination(BaseQueryPagination):
	def __init__(
		self,
		queried_list: list,
		page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = None,
        error_out: bool = True,
        count: bool = True,
		*args, **kwargs,
	):
		self.queried_list = queried_list
		super().__init__(
			page=page,
            per_page=per_page,
            max_per_page=max_per_page,
            error_out=error_out,
            count=count,
			*args, **kwargs
		)

	def _query_items(self):

		x = (self.page-1) * self.per_page
		y = x + self.per_page
		return self.queried_list[x:y]

	def _query_count(self) -> int:
		return len(self.queried_list)


def paginated_schema(schema):

	class PaginationSchema(Schema):
		page = fields.Integer()
		per_page = fields.Integer()
		items = fields.Nested(schema, many=True)
		total = fields.Integer()

	return PaginationSchema()

def search_query(model, model_attribute, search_str: str):

	tags: list[model] = model.query.filter(model_attribute.contains(search_str)).all()

	for word in search_str.split(" "):
		query:list[Query] = model.query.filter(model_attribute.contains(word)).all()
		tags.extend(q for q in query if q not in tags)

	return tags



class SortedList(list):...


class KeySortedList:
	def __init__(self, key: str) -> None:
		self.key = key
		self.l1 = []
		self.l2 = []
		self.l3 = []
