
# SPDX-License-Identifier: MIT
# --------------------------------------------------------------
#|																|
#|             Copyright 2023 - 2023, Amulya Paritosh			|
#|																|
#|  This file is part of Component Library Plugin for FreeCAD.	|
#|																|
#|               This file was created as a part of				|
#|              Google Summer Of Code Program - 2023			|
#|																|
# --------------------------------------------------------------

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY")
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
