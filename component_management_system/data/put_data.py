import csv

from werkzeug.exceptions import NotAcceptable

from ..licenses.models import SPDX
from ..licenses.operations import create as create_license
from ..tags.operations import create as create_tag


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
					"identifier" : row[1],
					"fsf_free" : True if row[2] == "Y" else False,
					"osi_approved" : True if row[3] == "Y" else False,
					"license_page" : row[4],
				}

				try:
					create_license(data)
				except NotAcceptable:
					pass


def db_tags_entry(tags_file_path):
	with open(tags_file_path, "r") as file:
		tags = file.readlines()

	tags = [t.replace("\n", "") for t in tags]


	for tag in tags:
		tag.strip()
		try:
			create_tag({"label": tag})
		except NotAcceptable:
			pass
