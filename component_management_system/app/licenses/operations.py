from typing import Literal

from flask import abort

from .models import SPDX
from .schemas import spdx_schema, spdxs_schema


def read_all() -> list[dict[str, str]]:
	licenses: list[SPDX] = SPDX.query.all()
	return spdxs_schema.dump(licenses)


def read_one(pk) -> tuple[dict[str, str], Literal[200]]:
	license: SPDX | None = SPDX.query.filter(SPDX.id==pk).one_or_none()

	if license is None:
		abort(404, f"License with id {pk} not found!")

	return spdx_schema.dump(license), 200 # type: ignore

def create(spdx_license) -> tuple[dict[str, str], Literal[201]]:
	existing_license = SPDX.query.filter(SPDX.fullname == spdx_license["fullname"]).one_or_none()

	if existing_license is not None:
		abort(406, f"License {spdx_license['fullname']} already exists")

	new_license: SPDX = spdx_schema.load(spdx_license)
	new_license.create()
	return spdx_schema.dump(new_license), 201 # type: ignore
