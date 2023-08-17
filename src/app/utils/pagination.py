
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

from dataclasses import dataclass

from flask_sqlalchemy.pagination import Pagination
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchemaMeta

MAX_PER_PAGE = 50

@dataclass()
class PsudoPagination:
	page: int
	per_page: int | None
	items: list
	total: int


class QueryPagination(Pagination):
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


def paginated_schema(schema: SQLAlchemyAutoSchemaMeta|Schema):

	class PaginationSchema(Schema):
		page = fields.Integer()
		per_page = fields.Integer()
		items = fields.Nested(schema, many=True)
		total = fields.Integer()

	return PaginationSchema()
