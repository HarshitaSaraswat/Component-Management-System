from typing import Literal

from flask import Response, abort, make_response

from ..utils import paginated_schema
from .models import Component, ComponentType
from .schemas import component_schema, components_schema


def read_all():
	query: list[Component] = Component.query.all()
	return components_schema.dump(query)


def read_page(page=None, page_size=None, all_data=False) -> list[dict[str, str]]:
	query = Component.query.paginate(page=page, per_page=page_size, max_per_page=50)
	return paginated_schema(components_schema).dump(query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	component: Component | None = Component.query.filter(Component.id==pk).one_or_none()

	if component is None:
		abort(404, f"Component with id {pk} not found!")

	return component_schema.dump(component), 200 # type: ignore


def create(component) -> tuple[dict[str, str], Literal[201]]:
	url = component.get("url")
	type = component.get("type")
	metadata = component.get("metadata_id")

	component['type'] = ComponentType.serialize(component.get("type"))

	existing_component: Component | None = Component.query.filter(Component.url == url).one_or_none()

	if existing_component is not None:
		abort(406, f"Component with url:{url} already exists")

	new_component: Component = component_schema.load(component)
	new_component.save_to_db()

	return component_schema.dump(new_component), 201 # type: ignore


def delete(pk) -> Response:
	existing_component: Component | None = Component.query.filter(Component.id==pk).one_or_none()

	if existing_component is None:
		abort(404, f"Component with id {pk} not found")

	existing_component.remove_from_db()
	return make_response(f"{existing_component.url}:{pk} successfully deleted", 200)
