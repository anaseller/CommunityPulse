# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine.interfaces import DBAPIType
#
# from src.core.config import settings
#
# # INIT DB
# db = SQLAlchemy()
#
#
# # INIT ROUTES


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.config import settings

# INIT DB
db = SQLAlchemy()


def init_database(app: Flask) -> None:
    db.init_app(app)


# INIT ROUTES
def register_routes(app: Flask) -> None:
    # from src.api.routes import register_api_routes
    # register_api_routes(app)
    ...


# INIT APP
def create_app() -> Flask:
    app = Flask(settings.APP_NAME)

    app.config.update(settings.get_flask_config())

    init_database(app=app)
    register_routes(app=app)

    return app
