#!.venv/bin/python

from werkzeug.serving import is_running_from_reloader

from component_management_system import FlaskApp, create_app
from component_management_system.database.utils import reset_db

connex_app: FlaskApp = create_app()

with connex_app.app.app_context(): # type: ignore
	if is_running_from_reloader():
		# reset_db()

		pass
	import json

	from component_management_system.components.operations import read

	data = read(
		# tags=["accesories", "wood", "stl", "switch", "electrical parts"],
		page=1,
		page_size=10,
		# file_types=["step"],
		sort_by="name",
		sort_ord="desc",
		columns=["name"],
		search_key="glass window",
	)
	print(json.dumps(data, indent=4))


connex_app.run()
