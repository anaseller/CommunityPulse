from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from src.core.config import settings

# INIT DB
db = SQLAlchemy()


def init_database(app: Flask) -> None:
    db.init_app(app)


# INIT ROUTES
def register_routes(app: Flask) -> None:
    from src.api.routes import register_blueprints
    register_blueprints(app)


# INIT APP
def create_app() -> Flask:
    app = Flask(settings.APP_NAME)

    app.config.update(settings.get_flask_config())
    alemb = Migrate()

    alemb.init_app(app, db)
    init_database(app=app)
    register_routes(app=app)

    return app