from typing import Literal

from flask import Response, abort, make_response

from ..utils import PsudoPagination, paginated_schema, search_query
from .models import Tag
from .schemas import tag_schema, tags_schema


def read_all():
	query: list[Tag] = Tag.query.all()
	psudo_paged_query = PsudoPagination(0, None, query, len(query))
	return paginated_schema(tags_schema).dump(psudo_paged_query)


def read_page(page=None, page_size=None):
	if not all((page, page_size)):
		return read_all()
	query = Tag.query.paginate(page=page, per_page=page_size, max_per_page=50)
	return paginated_schema(tags_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	tag: Tag | None = Tag.query.filter(Tag.id==pk).one_or_none()

	if tag is None:
		abort(404, f"Tag with id {pk} not found!")
	return tag_schema.dump(tag), 200 # type: ignore


def create(tag) -> tuple[dict[str, str], Literal[201]]:
	label: str = tag.get("label")
	existing_tag: Tag | None = Tag.query.filter(Tag.label==label).one_or_none()

	if existing_tag is not None:
		abort(406, f"Tag with label {label} already exists")

	new_tag: Tag = tag_schema.load(tag)
	new_tag.create()
	return tag_schema.dump(new_tag), 201 # type: ignore


def delete(pk) -> Response:
	existing_tag: Tag | None = Tag.query.filter(Tag.id==pk).one_or_none()

	if existing_tag is None:
		abort(404, f"Tag with id {pk} not found")

	existing_tag.delete()
	return make_response(f"{existing_tag.label}:{pk} successfully deleted", 200)


def get_metadatas(tag):
	existing_tag: Tag | None = Tag.query.filter(Tag.label==tag).one_or_none()

	if existing_tag is not None:
		print(existing_tag.metadatas)
	else:
		print(existing_tag)


def search(search_key):
	tags = search_query(Tag, Tag.label, search_key)
	return tags_schema.dump(tags)
