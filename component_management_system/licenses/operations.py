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
