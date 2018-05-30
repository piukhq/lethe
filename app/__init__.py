from flask import Flask

import settings


def create_app(config_name="settings"):
    from app.views import frontend, internal

    app = Flask(
        __name__,
        static_folder='static',
        static_url_path=settings.STATIC_URL)
    app.config.from_object(config_name)
    app.register_blueprint(internal)
    app.register_blueprint(frontend)

    return app
