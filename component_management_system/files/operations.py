from typing import Literal

from flask import Response, abort, make_response

from ..utils import paginated_schema
from .models import File, FileType
from .schemas import file_schema, files_schema


def read_all():
	query: list[File] = File.query.all()
	return files_schema.dump(query)


def read_page(page=None, page_size=None, all_data=False) -> list[dict[str, str]]:
	query = File.query.paginate(page=page, per_page=page_size, max_per_page=50)
	return paginated_schema(files_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	file: File | None = File.query.filter(File.id==pk).one_or_none()

	if file is None:
		abort(404, f"File with id {pk} not found!")

	return file_schema.dump(file), 200 # type: ignore


def create(file) -> tuple[dict[str, str], Literal[201]]:
	url = file.get("url")
	type = file.get("type")
	metadata = file.get("metadata_id")

	file['type'] = FileType.serialize(file.get("type"))

	existing_file: File | None = File.query.filter(File.url == url).one_or_none()

	if existing_file is not None:
		abort(406, f"File with url:{url} already exists")

	new_file: File = file_schema.load(file)
	new_file.save_to_db()

	return file_schema.dump(new_file), 201 # type: ignore


def delete(pk) -> Response:
	existing_file: File | None = File.query.filter(File.id==pk).one_or_none()

	if existing_file is None:
		abort(404, f"File with id {pk} not found")

	existing_file.remove_from_db()
	return make_response(f"{existing_file.url}:{pk} successfully deleted", 200)
