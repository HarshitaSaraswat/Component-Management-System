
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
	query: list[SPDX] = SPDX.query.all()
	psudo_paged_query = PsudoPagination(0, None, query, len(query))
	return paginated_schema(spdxs_schema).dump(psudo_paged_query)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	license: SPDX | None = SPDX.query.filter(SPDX.id==pk).one_or_none()

	if license is None:
		abort(404, f"License with id {pk} not found!")

	return spdx_schema.dump(license), 200

def create(spdx_license) -> tuple[dict[str, str], Literal[201]]:
	existing_license = SPDX.query.filter(SPDX.fullname == spdx_license["fullname"]).one_or_none()

	if existing_license is not None:
		abort(406, f"License {spdx_license['fullname']} already exists")

	new_license: SPDX = spdx_schema.load(spdx_license)
	new_license.create()
	return spdx_schema.dump(new_license), 201
