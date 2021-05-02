import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import threading
from project.networking.query import helperThreadFunction

#Show pipeline - meeting
#Preparation before meeting

#Set up Flask application
application = Flask(__name__)

#Set secret key for forms
application.config["SECRET_KEY"] = "mysecret"

##################################################
                #Set up database#
##################################################
basedir = os.path.abspath(os.path.dirname(__file__))
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)
Migrate(application, db)

##################################################
                #Login configurations#
##################################################
loginManager = LoginManager()

loginManager.init_app(application)

loginManager.login_view = "users.login"

#Register blueprint in project/core/views.py
from project.core.views import core
application.register_blueprint(core)


#Register blueprint in project/users/views.py
from project.users.views import users
application.register_blueprint(users)

threading.Thread(target=helperThreadFunction).start()
