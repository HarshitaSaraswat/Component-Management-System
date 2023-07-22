from typing import Literal
from werkzeug.datastructures import FileStorage
from flask import Response, abort, make_response, request
from ..utils import PsudoPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE
from .models import File, FileType
from .schemas import file_schema, files_schema
from .github import upload_new_file

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


def create(file_data, metadata_id=None) -> tuple[dict[str, str], Literal[201]]:
	url = file_data.get("url")

	file_data['type'] = FileType.serialize(file_data.get("type"))

	existing_file: File | None = File.query.filter(File.url == url).one_or_none()

	if existing_file is not None:
		abort(406, f"File with url:{url} already exists")

	if metadata_id is not None:
		file_data["metadata_id"] = metadata_id

	new_file: File = file_schema.load(file_data)
	new_file.create()

	return file_schema.dump(new_file), 201 # type: ignore


def delete(pk) -> Response:
	existing_file: File | None = File.query.filter(File.id==pk).one_or_none()

	if existing_file is None:
		abort(404, f"File with id {pk} not found")

	existing_file.delete()
	return make_response(f"{existing_file.url}:{pk} successfully deleted", 200)


def upload_to_github(upload_info):
	files = request.files.getlist('file')
	access_token = request.headers.get("X-Access-Token", "")

	for file in files:
		content_file= upload_new_file(
			access_token,
			upload_info.get("repository"),
			upload_info.get("branch"),
			file.stream.read(),
			file.filename,
		)
		print(f"{content_file.download_url=}; {content_file.size=}")

	return make_response("recirved files", 201)
