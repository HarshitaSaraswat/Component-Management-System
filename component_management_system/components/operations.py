from database import db
from flask import abort, make_response

from .models import Component, ComponentType
from .schemas import component_schema, components_schema


def read_all():
	components = Component.query.all()
	return components_schema.dump(components)


def read_one(pk):
	component = Component.query.filter(Component.id==pk).one_or_none()

	if component is None:
		abort(404, f"Component with id {pk} not found!")

	return component_schema.dump(component), 200


def create(component):
	url = component.get("url")
	type = component.get("type")

	component['type'] = ComponentType.serialize(component.get("type"))

	existing_component = Component.query.filter(Component.url == url).one_or_none()

	if existing_component is not None:
		abort(406, f"Component with url:{url} exists")

	new_component = component_schema.load(component, session=db.session)
	db.session.add(new_component)
	db.session.commit()
	return component_schema.dump(new_component), 201


def delete(pk):
	existing_component = Component.query.filter(Component.id==pk).one_or_none()

	if existing_component is None:
		abort(404, f"Component with id {pk} not found")

	db.session.delete(existing_component)
	db.session.commit()
	return make_response(f"{existing_component.url}:{pk} successfully deleted", 200)
