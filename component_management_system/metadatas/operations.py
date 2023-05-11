from database import db
from flask import abort, make_response

from .models import Metadata
from .schemas import metadata_schema, metadatas_schema
from tags.models import Tag
from tags.schemas import tags_schema
from components.schemas import components_schema

def read_all():
	metadatas = Metadata.query.all()
	return metadatas_schema.dump(metadatas)


def read_one(pk):
	metadata = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if metadata is None:
		abort(404, f"Metadata with id {pk} not found!")

	return metadata_schema.dump(metadata), 200


def create(metadata):
	# url = metadata.get("url")

	# existing_metadata = Metadata.query.filter(Metadata.url == url).one_or_none()

	# if existing_metadata is not None:
	# 	abort(406, f"Metadata with url:{url} exists")

	new_metadata = metadata_schema.load(metadata, session=db.session)
	db.session.add(new_metadata)
	db.session.commit()
	return metadata_schema.dump(new_metadata), 201


def delete(pk):
	existing_metadata = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	db.session.delete(existing_metadata)
	db.session.commit()
	return make_response(f"metadata:{pk} successfully deleted", 200)


def read_tags(pk):
	existing_metadata = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	return tags_schema.dump(existing_metadata.tags)


def add_tags(pk, tags):
	existing_metadata = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	for tag in tags:
		existing_tag = Tag.query.filter(Tag.label==tag).one_or_none()

		if existing_tag is None:
			print(f"tag {tag} does not exist!")

		existing_metadata.tags.append(existing_tag)
		db.session.commit()

	return make_response(f"tags added successfully", 200)


def read_components(pk):
	existing_metadata = Metadata.query.filter(Metadata.id==pk).one_or_none()

	if existing_metadata is None:
		abort(404, f"Metadata with id {pk} not found")

	return components_schema.dump(existing_metadata.components)
