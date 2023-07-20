from os import path

from ...config import basedir
from .base import db, es


def clear_db():
	db.drop_all()
	es.options(ignore_status=[400,404]).indices.delete(index='metadatas')


def clear_data():
	db.drop_all()
	db.create_all()


def pre_entry():
	from .data.put_data import (db_license_entry, db_metadata_entry,
	                            db_metadata_file_entry, db_tags_entry)

	print("creating license entries...")
	db_license_entry(path.join(basedir,"app/database/data/spdx_license.csv"))
	print("licnses entry complete")

	print("creating Tag entries...")
	db_tags_entry(path.join(basedir,"app/database/data/tags.txt"))
	print("Tags entry complete")

	print("creating Metadata and Files entries...")
	db_metadata_file_entry(path.join(basedir,"app/database/data/files.json"))
	print("Metadatas and Files entry complete")

	# print("creating Component entries...")
	# db_component_entry(basedir+"app/database/data/files.json")
	# print("Components entry complete")


def reset_db():
	clear_data()
	pre_entry()
