from typing import Literal

from flask import Response, abort, make_response
from sqlalchemy.exc import IntegrityError

from ..database import db
from ..utils import paginated_schema
from .models import Component, ComponentType
from .schemas import component_schema, components_schema


def read(page=None, page_size=None, all_data=False) -> list[dict[str, str]]:
	if all_data:
		query: list[Component] = Component.query.all()
		return components_schema.dump(query)
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

	new_component = component_schema.load(component, session=db.session)
	db.session.add(new_component)

	try:
		db.session.commit()
	except IntegrityError:
		abort(406, f"Component on metadata:{metadata} with type:{type} already exists")

	return component_schema.dump(new_component), 201 # type: ignore


def delete(pk) -> Response:
	existing_component: Component | None = Component.query.filter(Component.id==pk).one_or_none()

	if existing_component is None:
		abort(404, f"Component with id {pk} not found")

	db.session.delete(existing_component)
	db.session.commit()
	return make_response(f"{existing_component.url}:{pk} successfully deleted", 200)
