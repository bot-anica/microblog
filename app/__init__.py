import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from elasticsearch import Elasticsearch
from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


def get_locale():
    # return 'ru'
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


db = SQLAlchemy()  # init SQLAlchemy for Flask-SQLAlchemy
migrate = Migrate()  # init Migrate for Flask-Migrate

login = LoginManager()  # init LoginManager for Flask-Login
login.login_view = 'auth.login'  # redirect to login page if user is not logged in
login.login_message = _l('Please log in to access this page.')

mail = Mail()
moment = Moment()
babel = Babel()

elasticsearch_config = []


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']], api_key=app.config['ELASTICSEARCH_API_KEY']) if app.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
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

    return app


from app import models
from app.main import routes
