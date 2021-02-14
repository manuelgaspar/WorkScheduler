from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

WorkScheduler = Flask(__name__)
WorkScheduler.config.from_object(Config)
db = SQLAlchemy(WorkScheduler)
migrate = Migrate(WorkScheduler, db)

from app import routes, models