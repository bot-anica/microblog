import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None

        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = None

        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)

        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

db = SQLAlchemy(app)  # init SQLAlchemy for Flask-SQLAlchemy
migrate = Migrate(app, db)  # init Migrate for Flask-Migrate

login = LoginManager(app)  # init LoginManager for Flask-Login
login.login_view = 'login'  # redirect to login page if user is not logged in

mail = Mail(app)

from app import routes, models, errors
