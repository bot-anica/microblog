from flask import render_template

from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    # Чтобы убедиться, что неудачные сеансы базы данных не мешают доступу к базе данных,
    # вызванным шаблоном, я выдаю откат сеанса
    db.session.rollback()
    return render_template('errors/500.html'), 500
