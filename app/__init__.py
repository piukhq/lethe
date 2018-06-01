from flask import Flask
from flask_cdn import CDN

import settings


def create_app(config_name="settings"):
    from app.views import frontend, internal

    cdn = CDN()

    app = Flask(
        __name__,
        static_folder='static',
        static_url_path=settings.STATIC_URL)
    app.config.from_object(config_name)
    app.register_blueprint(internal)
    app.register_blueprint(frontend)

    cdn.init_app(app)

    return app
