from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy(app)  # init SQLAlchemy for Flask-SQLAlchemy
migrate = Migrate(app, db)  # init Migrate for Flask-Migrate

login = LoginManager(app)  # init LoginManager for Flask-Login
login.login_view = 'login'  # redirect to login page if user is not logged in

from app import routes, models
