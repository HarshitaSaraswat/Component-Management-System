from component_management_system import FlaskApp, create_app
from component_management_system.database.utils import pre_entry, reset_db

connex_app: FlaskApp = create_app()

with connex_app.app.app_context(): # type: ignore
	# from component_management_system.data.put_data import db_metadata_entry
	# db_metadata_entry("component_management_system/data/files.json")
	# pre_entry()
	reset_db()

connex_app.run()
