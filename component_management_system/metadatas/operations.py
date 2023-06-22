from os import read
from typing import Literal

from flask import Response, abort, make_response

from ..files.schemas import files_schema
from ..tags.models import Tag
from ..tags.schemas import tags_schema
from ..utils import PsudoPagination, paginated_schema, search_query
from ..utils import paginated_schema, search_query
from .models import Metadata
from .schemas import metadata_schema, metadatas_schema


def read_all():
	query: list[Metadata] = Metadata.query.all()
	psudo_paged_query = PsudoPagination(0, None, query, len(query))
	return paginated_schema(metadatas_schema).dump(psudo_paged_query)


def read_page(page=None, page_size=None):
	if not all((page, page_size)):
		return read_all()

	query = Metadata.query.paginate(page=page, per_page=page_size, max_per_page=50)
	return paginated_schema(metadatas_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if metadata is None:
		abort(404, f"Metadata with id {pk} not found!")

	return metadata_schema.dump(metadata), 200 # type: ignore


def create(metadata) -> tuple[dict[str, str], Literal[201]]:
	existing_metadata = Metadata.query.filter(Metadata.name == metadata.get("name")).one_or_none()

	if existing_metadata is not None:
		abort(406, f"This Metadata already exists")

	new_metadata: Metadata = metadata_schema.load(metadata)
	new_metadata.save_to_db()
	return metadata_schema.dump(new_metadata), 201 # type: ignore


def delete(pk) -> Response:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	existing_metadata.remove_from_db()
	return make_response(f"metadata:{pk} successfully deleted", 200)


def read_tags(pk) -> list[dict[str, str]]:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	return tags_schema.dump(existing_metadata.tags)


def add_tags(pk, tags) -> Response:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	for tag in tags:
		existing_tag: Metadata | None = Tag.query.filter(Tag.label==tag).one_or_none()

		if existing_tag is None:
			abort(404, f"tag {tag} does not exist!")

		existing_metadata.add_tag(existing_tag)

	return make_response(f"tags added successfully", 200)


def read_files(pk) -> list[dict[str, str]]:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	return files_schema.dump(existing_metadata.files)


def search(search_key):
	metadatas = search_query(Metadata, Metadata.name, search_key)
	return metadatas_schema.dump(metadatas)
