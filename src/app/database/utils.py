
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

from os import path

from ...config import basedir
from ...logger import logger
from .base import db, es


def clear_db() -> None:
	"""
	Clears the database and Elasticsearch.

	Returns:
		None
	"""

	db.drop_all()
	es.options(ignore_status=[400,404]).indices.delete(index='metadatas')


def clear_data() -> None:
	"""
	Clears the data in the database.

	Returns:
		None
	"""

	db.drop_all()
	db.create_all()


def pre_entry() -> None:
	"""
	Performs pre-entry operations by creating license, tag, metadata, and file entries in the database.

	Returns:
		None
	"""

	from .data.put_data import (db_license_entry, db_metadata_entry,
	                            db_metadata_file_entry, db_tags_entry)

	logger.info("creating license entries...")
	db_license_entry(path.join(basedir,"app/database/data/spdx_license.csv"))
	logger.info("licnses entry complete")

	logger.info("creating Tag entries...")
	db_tags_entry(path.join(basedir,"app/database/data/tags.txt"))
	logger.info("Tags entry complete")

	logger.info("creating Metadata and Files entries...")
	db_metadata_file_entry(path.join(basedir,"app/database/data/files.json"))
	logger.info("Metadatas and Files entry complete")

	# logger.info("creating Component entries...")
	# db_component_entry(basedir+"app/database/data/files.json")
	# logger.info("Components entry complete")


def reset_db() -> None:
	"""
	Resets the database by clearing the data and performing pre-entry operations.

	Returns:
		None
	"""

	clear_data()
	pre_entry()
