from component_management_system import FlaskApp, create_app

connex_app: FlaskApp = create_app()

with connex_app.app.app_context(): # type: ignore
	pass

connex_app.run()
