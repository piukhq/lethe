import sentry_sdk

from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from . import settings


def create_app(config_name: str = "lethe.settings") -> Flask:
    from lethe.version import __version__
    from lethe.views import frontend, internal

    _app = Flask(__name__, static_folder="static", static_url_path=settings.STATIC_URL)
    _app.config.from_object(config_name)

    _app.register_blueprint(internal)
    _app.register_blueprint(frontend)

    sentry_sdk.init(integrations=[FlaskIntegration()], release=__version__)

    return _app


app = create_app()
