from typing import Literal

from flask import Response, abort, make_response

from ..utils import PsudoPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE
from .models import File, FileType
from .schemas import file_schema, files_schema


def read_all():
	query: list[File] = File.query.all()
	psudo_paged_query = PsudoPagination(0, None, query, len(query))
	return paginated_schema(files_schema).dump(psudo_paged_query)


def read_page(page=None, page_size=None) -> list[dict[str, str]]:
	if not all((page, page_size)):
		return read_all()

	query = File.query.paginate(page=page, per_page=page_size, max_per_page=MAX_PER_PAGE)
	return paginated_schema(files_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	file: File | None = File.query.filter(File.id==pk).one_or_none()

	if file is None:
		abort(404, f"File with id {pk} not found!")

	return file_schema.dump(file), 200 # type: ignore


def create(metadata_id, file) -> tuple[dict[str, str], Literal[201]]:
	url = file.get("url")

	file['type'] = FileType.serialize(file.get("type"))

	existing_file: File | None = File.query.filter(File.url == url).one_or_none()

	if existing_file is not None:
		abort(406, f"File with url:{url} already exists")

	file["metadata_id"] = metadata_id

	new_file: File = file_schema.load(file)
	new_file.create()

	return file_schema.dump(new_file), 201 # type: ignore


def delete(pk) -> Response:
	existing_file: File | None = File.query.filter(File.id==pk).one_or_none()

	if existing_file is None:
		abort(404, f"File with id {pk} not found")

	existing_file.delete()
	return make_response(f"{existing_file.url}:{pk} successfully deleted", 200)
