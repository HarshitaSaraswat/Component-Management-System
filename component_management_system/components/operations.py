from typing import Literal

from database import db
from flask import Response, abort, make_response

from .models import Component, ComponentType
from .schemas import component_schema, components_schema


def read_all() -> list[dict[str, str]]:
	components: list[Component] = Component.query.all()
	return components_schema.dump(components)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	component: Component | None = Component.query.filter(Component.id==pk).one_or_none()

	if component is None:
		abort(404, f"Component with id {pk} not found!")

	return component_schema.dump(component), 200 # type: ignore


def create(component) -> tuple[dict[str, str], Literal[201]]:
	url = component.get("url")

	component['type'] = ComponentType.serialize(component.get("type"))

	existing_component: Component | None = Component.query.filter(Component.url == url).one_or_none()

	if existing_component is not None:
		abort(406, f"Component with url:{url} exists")

	new_component = component_schema.load(component, session=db.session)
	db.session.add(new_component)
	db.session.commit()
	return component_schema.dump(new_component), 201 # type: ignore


def delete(pk) -> Response:
	existing_component: Component | None = Component.query.filter(Component.id==pk).one_or_none()

	if existing_component is None:
		abort(404, f"Component with id {pk} not found")

	db.session.delete(existing_component)
	db.session.commit()
	return make_response(f"{existing_component.url}:{pk} successfully deleted", 200)
