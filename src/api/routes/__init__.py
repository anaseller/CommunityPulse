from flask import Flask

from src.api.routes.poll import polls_blueprint


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(polls_blueprint)