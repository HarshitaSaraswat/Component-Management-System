from typing import Literal

from flask import Response, abort, make_response

from ..components.schemas import components_schema
from ..database import db
from ..tags.models import Tag
from ..tags.schemas import tags_schema
from .models import Metadata
from .schemas import metadata_schema, metadatas_schema


def read_all() -> list[dict[str, str]]:
	metadatas: list[Metadata] = Metadata.query.all()
	return metadatas_schema.dump(metadatas)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if metadata is None:
		abort(404, f"Metadata with id {pk} not found!")

	return metadata_schema.dump(metadata), 200 # type: ignore


def create(metadata) -> tuple[dict[str, str], Literal[201]]:
	# url = metadata.get("url")

	# existing_metadata = Metadata.query.filter(Metadata.url == url).one_or_none()

	# if existing_metadata is not None:
	# 	abort(406, f"Metadata with url:{url} exists")

	new_metadata: Metadata = metadata_schema.load(metadata, session=db.session)
	db.session.add(new_metadata)
	db.session.commit()
	return metadata_schema.dump(new_metadata), 201 # type: ignore


def delete(pk) -> Response:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	db.session.delete(existing_metadata)
	db.session.commit()
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
			print(f"tag {tag} does not exist!")

		existing_metadata.tags.append(existing_tag)
		db.session.commit()

	return make_response(f"tags added successfully", 200)


def read_components(pk) -> list[dict[str, str]]:
	existing_metadata: Metadata | None = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	return components_schema.dump(existing_metadata.components)
