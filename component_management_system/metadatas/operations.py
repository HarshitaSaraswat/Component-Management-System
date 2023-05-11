from database import db
from flask import abort, make_response

from .models import Metadata
from .schemas import metadata_schema, metadatas_schema


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
