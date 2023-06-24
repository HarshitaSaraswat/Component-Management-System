from dataclasses import dataclass

from flask_sqlalchemy.pagination import QueryPagination as BaseQueryPagination
from marshmallow import Schema, fields

MAX_PER_PAGE = 50

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
        max_per_page: int = MAX_PER_PAGE,
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
