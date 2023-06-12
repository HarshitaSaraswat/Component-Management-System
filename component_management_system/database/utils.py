from .db import db


def clear_db():
	db.drop_all()


def clear_data():
	db.drop_all()
	db.create_all()


def pre_entry():
	from component_management_system.database.data.put_data import (db_license_entry,
	                                                       db_tags_entry, db_metadata_entry)

	print("creating license entries...")
	db_license_entry("component_management_system/database/data/spdx_license.csv")
	print("licnses entry complete")

	print("creating Tag entries...")
	db_tags_entry("component_management_system/database/data/tags.txt")
	print("Tags entry complete")

	print("creating Metadata entries...")
	db_metadata_entry("component_management_system/database/data/files.json")
	print("Metadatas entry complete")


def reset_db():
	clear_data()
	pre_entry()
