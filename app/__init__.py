from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

WorkScheduler = Flask(__name__)
WorkScheduler.config.from_object(Config)
db = SQLAlchemy(WorkScheduler)
migrate = Migrate(WorkScheduler, db)
login = LoginManager(WorkScheduler)
login.login_view = 'login'
bootstrap = Bootstrap(WorkScheduler)

from app import routes, models