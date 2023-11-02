from flask import Flask


def create_routes(app: Flask):

	@app.route('/')
	def root_route():
		app.logger.debug("A debug message")
		app.logger.info("An info message")
		app.logger.warning("A warning message")
		app.logger.error("An error message")
		app.logger.critical("A critical message")

		return "Hello, World!"
