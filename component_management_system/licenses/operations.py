from typing import Literal

from flask import abort
from sqlalchemy.exc import IntegrityError

from ..database import db
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

def create(spdx_license):
	if SPDX.query.filter(SPDX.fullname == spdx_license["fullname"]).one_or_none() is not None:
		abort(406, f"License {spdx_license['fullname']} already exists")

	new_license = spdx_schema.load(spdx_license, session=db.session)
	db.session.add(new_license)

	try:
		db.session.commit()
	except IntegrityError:
		abort(406, f"License {spdx_license['fullname']} already exists")

	return spdx_schema.dump(new_license), 201 # type: ignore
