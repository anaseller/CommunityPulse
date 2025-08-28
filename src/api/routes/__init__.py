from flask import Flask, Blueprint

from src.api.routes.poll import polls_blueprint
from src.api.routes.category import categories_blueprint


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(polls_blueprint)
    app.register_blueprint(categories_blueprint)
