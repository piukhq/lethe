from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from flask_cdn import CDN
import sentry_sdk

import settings

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
        from app.version import __version__
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            environment=app.config['SENTRY_ENV'],
            integrations=[
                FlaskIntegration()
            ],
            release=__version__
        )

    return app
