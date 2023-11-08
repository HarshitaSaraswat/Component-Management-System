
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

from typing import Literal

from flask import abort

from ..utils import PsudoPagination, paginated_schema
from .models import SPDX
from .schemas import spdx_schema, spdxs_schema


def read_all():
	"""
	Reads all SPDX licenses from the database and returns the paginated result.

	This function queries all SPDX licenses from the database using `SPDX.query.all()`.
	It then creates a `PsudoPagination` object with the query results and the total count.
	Finally, it applies pagination to the result using the `paginated_schema` function and returns the serialized result.

	Returns:
		dict: The paginated result of SPDX licenses.

	Example:
		```python
		result = read_all()
		print(result)
		```
	"""

	query: list[SPDX] = SPDX.query.all()
	psudo_paged_query = PsudoPagination(0, None, query, len(query))
	return paginated_schema(spdxs_schema).dump(psudo_paged_query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	"""
	Reads a single SPDX license from the database based on the provided primary key.

	This function queries the SPDX license with the given primary key from the database using `SPDX.query.filter(SPDX.id==pk).one_or_none()`.
	If the license is not found, a 404 error is raised.
	Otherwise, the license is serialized using the `spdx_schema` and returned along with a status code of 200.

	Args:
		pk: The primary key of the SPDX license to read.

	Returns:
		tuple[dict[str, str], Literal[200]]: A tuple containing the serialized SPDX license and the status code 200.

	Raises:
		HTTPException: Raised when the license with the given primary key is not found.

	Example:
		```python
		result = read_one(1)
		print(result)
		```
	"""

	license: SPDX | None = SPDX.query.filter(SPDX.id==pk).one_or_none()

	if license is None:
		abort(404, f"License with id {pk} not found!")

	return spdx_schema.dump(license), 200

def create(spdx_license) -> tuple[dict[str, str], Literal[201]]:
	"""
	Creates a new SPDX license in the database.

	This function checks if a license with the same fullname already exists in the database.
	If an existing license is found, a 406 error is raised.
	Otherwise, the provided SPDX license data is deserialized using the `spdx_schema` and a new license is created in the database.
	The serialized license is then returned along with a status code of 201.

	Args:
		spdx_license (dict[str, str]): The SPDX license data to create.

	Returns:
		tuple[dict[str, str], Literal[201]]: A tuple containing the serialized SPDX license and the status code 201.

	Raises:
		HTTPException: Raised when a license with the same fullname already exists.

	Example:
		```python
		license_data = {"fullname": "MIT License", "identifier": "MIT", "license_page": "https://opensource.org/licenses/MIT"}
		result = create(license_data)
		print(result)
		```
	"""

	existing_license = SPDX.query.filter(SPDX.fullname == spdx_license["fullname"]).one_or_none()

	if existing_license is not None:
		abort(406, f"License {spdx_license['fullname']} already exists")

	new_license: SPDX = spdx_schema.load(spdx_license)
	new_license.create()
	return spdx_schema.dump(new_license), 201
