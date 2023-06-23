#!.venv/bin/python

from werkzeug.serving import is_running_from_reloader

from component_management_system import FlaskApp, create_app
from component_management_system.database.utils import reset_db

connex_app: FlaskApp = create_app()

with connex_app.app.app_context(): # type: ignore
	if is_running_from_reloader():
		# reset_db()

		pass
	# from component_management_system.elastic_search import elastify

connex_app.run()
