#!.venv/bin/python

from dotenv import load_dotenv

from src.app.main import create_app

load_dotenv()

if __name__ == "__main__":
	app = create_app()
	app.run(host="127.0.0.1", port=5000, debug=True)
