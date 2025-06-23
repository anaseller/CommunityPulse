from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.interfaces import DBAPIType

from src.core.config import settings

# INIT DB
db = SQLAlchemy()


# INIT ROUTES