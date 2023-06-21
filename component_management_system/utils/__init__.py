from dataclasses import dataclass

from flask_sqlalchemy.query import Query
from marshmallow import Schema, fields


@dataclass()
class PsudoPagination:
	page: int
	per_page: int | None
	items: list
	total: int


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
