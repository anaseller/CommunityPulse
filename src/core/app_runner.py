from flask import Flask
from src.core.config import settings
from src.core.db import init_db


# INIT ROUTES
def register_routes(app: Flask) -> None:
    from src.api.routes import register_blueprints
    register_blueprints(app)


# INIT APP
def create_app() -> Flask:
    app = Flask(settings.APP_NAME)

    app.config.update(settings.get_flask_config())

    init_db(app)

    register_routes(app=app)

    return app