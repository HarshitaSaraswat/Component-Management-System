import csv
import json
import random
from sqlite3 import IntegrityError

from werkzeug.exceptions import NotAcceptable

from ...components.operations import create as create_component
from ...licenses.models import SPDX
from ...licenses.operations import create as create_license
from ...metadatas.models import Metadata
from ...metadatas.operations import add_tags
from ...metadatas.operations import create as create_meatdata
from ...tags.operations import create as create_tag


def db_license_entry(license_csv_path):
	with open(license_csv_path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				if SPDX.query.filter(SPDX.fullname == row[0]).one_or_none() is not None:
					continue

				data = {
					"fullname" : row[0],
					"identifier" : row[1].lower(),
					"fsf_free" : True if row[2] == "Y" else False,
					"osi_approved" : True if row[3] == "Y" else False,
					"license_page" : row[4],
				}

				try:
					new_license, _ = create_license(data)
					print("created License:", new_license["fullname"])
				except NotAcceptable:
					pass


def db_tags_entry(tags_file_path):
	with open(tags_file_path, "r") as file:
		tags = file.readlines()

	tags = [t.replace("\n", "").lower() for t in tags]


	for tag in tags:
		tag.strip()
		try:
			new_tag, _ = create_tag({"label": tag})
			print("created tag:", new_tag["label"])
		except NotAcceptable:
			pass


def _get_tags(components: dict) -> list[str]:

	any_key = list(components.keys())[0]
	url = components[any_key]["url"]
	*_, file_path = url.split('/', 6)
	file_path = file_path.replace("%20", " ").lower()
	return file_path.split('/')[:-1]


def _make_metadata(comp, data):

	metadata_data = {
		"name": comp.lower(),
		"version": "1",
		"maintainer": "FreeCAD@gmail.com",
		"author": "FreeCAD@gmail.com",
		"thumbnail": data["images"][0] if len(data["images"])!=0 else None,
		"description": None,
		"rating": random.randint(1, 5),
		"license_id" : "b89cd6361d7c446f85a5eb4de75534d5",
	}

	try:
		new_metadata, _ = create_meatdata(metadata_data)
		tags = _get_tags(data["components"])
		add_tags(new_metadata['id'], tags)
		print("created Metadata:", new_metadata["name"], "with tags:", tags)

	except NotAcceptable:
		pass


def _make_component(comp_name, data):

	for type_, info in data["components"].items():

		comp_name = comp_name.replace("%20", " ").lower()
		metadata: Metadata = Metadata.query.filter(Metadata.name == comp_name).one_or_none()

		comp_data = {
			"url" : info["url"],
			"type" : type_.lower(),
			"size" : info["size"],
			"metadata_id" : str(metadata.id),
		}

		try:
			new_comp, _ = create_component(comp_data)
			print("created Component:", metadata.name, "of type:", new_comp["type"])

		except NotAcceptable:
			pass

		except IntegrityError:
			raise


def _traverse(_dict: dict, traversed_names: set, funcs):

	for key, value in _dict.items():
		if key != "files":
			_traverse(value, traversed_names, funcs)

		else:
			for comp, data in value.items():

				if comp == "files": continue

				if comp in traversed_names: continue

				if len(data["components"].keys()) == 0:
					traversed_names.add(comp)
					continue

				traversed_names.add(comp)
				for func in funcs:
					func(comp, data)


def db_metadata_entry(metadata_file_oath):
	with open(metadata_file_oath, 'r') as file:
		data = json.load(file)

	traversed_names = set()
	_traverse(data, traversed_names, [_make_metadata])


def db_component_entry(file_path):
	with open(file_path, 'r') as file:
		data = json.load(file)

	traversed_names = set()
	_traverse(data, traversed_names, [_make_component])

def db_metadata_component_entry(file_path):
	with open(file_path, 'r') as file:
		data = json.load(file)

	traversed_names = set()
	_traverse(data, traversed_names, (_make_metadata, _make_component))
