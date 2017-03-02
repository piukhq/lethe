from flask import Flask


def create_app(config_name="settings"):
    from app.views import frontend

    app = Flask(__name__, static_folder='password')
    app.config.from_object(config_name)
    app.register_blueprint(frontend)

    return app
