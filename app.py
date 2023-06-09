from component_management_system import FlaskApp, create_app, db

connex_app: FlaskApp = create_app()

with connex_app.app.app_context(): # type: ignore
	db.create_all()

connex_app.run()
