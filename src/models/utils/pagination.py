
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
	"""
	Data class representing pagination information.

	Attributes:
		page (int): The current page number.
		per_page (int | None): The number of items per page, or None if not specified.
		items (list): The list of items on the current page.
		total (int): The total number of items.

	Example:
		```python
		pagination = PsudoPagination(page=1, per_page=10, items=[...], total=100)
		```
	"""

	page: int
	per_page: int | None
	items: list
	total: int


class QueryPagination(Pagination):
	"""
	A subclass of Pagination that provides querying functionality.

	Attributes:
		queried_list (list): The list of items to be paginated.

	Methods:
		_query_items: Retrieves the items for the current page.
		_query_count: Retrieves the total count of items.

	Example:
		```python
		pagination = QueryPagination(queried_list=[...], page=1, per_page=10)
		```
	"""

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
		"""
		Initializes a QueryPagination object.

		Args:
			queried_list (list): The list of items to be paginated.
			page (int | None, optional): The current page number. Defaults to None.
			per_page (int | None, optional): The number of items per page. Defaults to None.
			max_per_page (int, optional): The maximum number of items per page. Defaults to MAX_PER_PAGE.
			error_out (bool, optional): Whether to raise an error if the requested page is out of range. Defaults to True.
			count (bool, optional): Whether to include the total count of items. Defaults to True.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.
		"""

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
		"""
		Queries and retrieves the items for the current page.

		Returns:
			list: The items for the current page.
		"""

		x = (self.page-1) * self.per_page
		y = x + self.per_page
		return self.queried_list[x:y]

	def _query_count(self) -> int:
		"""
		Returns the count of items in the queried list.

		Returns:
			int: The count of items in the queried list.
		"""

		return len(self.queried_list)


def paginated_schema(schema: SQLAlchemyAutoSchemaMeta|Schema):
	"""
	Creates a pagination schema for the provided schema.

	Args:
		schema (SQLAlchemyAutoSchemaMeta | Schema): The schema to be nested within the pagination schema.

	Returns:
		PaginationSchema: The pagination schema.

	Example:
		```python
		user_schema = UserSchema()
		pagination_schema = paginated_schema(user_schema)
		```
	"""

	class PaginationSchema(Schema):
		"""
		A schema representing pagination information.

		Attributes:
			page (Integer): The current page number.
			per_page (Integer): The number of items per page.
			items (Nested): The nested schema representing the items on the current page.
			total (Integer): The total count of items.
		"""

		page = fields.Integer()
		per_page = fields.Integer()
		items = fields.Nested(schema, many=True)
		total = fields.Integer()

	return PaginationSchema()
