from typing import Literal

from flask import Response, abort, make_response, request
from werkzeug.datastructures import FileStorage

from ..metadatas.models import Metadata
from ..metadatas.schemas import metadata_schema
from ..utils import PsudoPagination, paginated_schema
from ..utils.pagination import MAX_PER_PAGE
from .github import get_repository, upload_new_file
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
	files = request.files.getlist('component_files')
	thumbnail_file: FileStorage = request.files.get('thumbnail_image') # type: ignore
	access_token = request.headers.get("X-Access-Token", "")

	metadata: Metadata | None = Metadata.query.filter(Metadata.id==upload_info.get("metadata_id")).one_or_none()
	if metadata is None:
		abort(404, f"Metadata with id {upload_info.get('metadata_id')} not found")

	repo = get_repository(access_token, upload_info.get("repository"))

	response = {
		"files" : [],
		"metadata" : None,
	}
	for file in files:
		content = upload_new_file(
			repo,
			upload_info.get("branch"),
			file.stream.read(),
			f"{metadata.name}/{file.filename}",
		)

		resp, _ = create({
			"metadata_id": str(metadata.id),
			"size": content.size,
			"type": file.filename.rsplit('.', 1)[-1],
			"url": content.download_url,
		})
		response["files"].append(resp)

	content = upload_new_file(
		repo,
		upload_info.get("branch"),
		thumbnail_file.stream.read(),
		f"{metadata.name}/thumbnail.{thumbnail_file.filename.rsplit('.', 1)[-1]}",
	)
	metadata.thumbnail = content.download_url # type: ignore
	metadata.commit()
	response["metadata"] = metadata_schema.dump(metadata)

	return response, 201
