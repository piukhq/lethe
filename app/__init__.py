import os

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

import settings


def create_app(config_name='settings'):
    from app.views import frontend, internal
    from app.version import __version__

    app = Flask(
        __name__,
        static_folder='static',
        static_url_path=settings.STATIC_URL)
    app.config.from_object(config_name)

    app.register_blueprint(internal)
    app.register_blueprint(frontend)


    sentry_sdk.init(
        integrations=[
            FlaskIntegration()
        ],
        release=__version__
    )

    return app
