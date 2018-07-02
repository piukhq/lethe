import logging

from flask import Flask
from flask_cdn import CDN
from raven.contrib.flask import Sentry

from .version import __version__
import settings

sentry = Sentry()
cdn = CDN()


def create_app(config_name='settings'):
    from app.views import frontend, internal

    app = Flask(
        __name__,
        static_folder='static',
        static_url_path=settings.STATIC_URL)
    app.config.from_object(config_name)

    app.register_blueprint(internal)
    app.register_blueprint(frontend)

    cdn.init_app(app)

    if app.config.get('SENTRY_DSN'):
        sentry.init_app(
            app,
            dsn=app.config['SENTRY_DSN'],
            logging=True,
            level=logging.ERROR)
        sentry.client.release = __version__

    return app
