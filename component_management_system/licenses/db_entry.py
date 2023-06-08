import csv

from ..database import db
from .schemas import spdx_schema


def make_db_entry():
	with open('/home/encryptedbee/tesla/projects/GSOC/Component_Management_System/component_management_system/licenses/spdx_license.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				data = {
					"fullname" : row[0],
					"identifier" : row[1],
					"fsf_free" : True if row[2] == "Y" else False,
					"osi_approved" : True if row[3] == "Y" else False,
					"license_page" : row[4],
				}
				new_license = spdx_schema.load(data, session=db.session)
				db.session.add(new_license)
		db.session.commit()
