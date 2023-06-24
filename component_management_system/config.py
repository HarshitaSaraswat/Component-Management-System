import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY")
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
