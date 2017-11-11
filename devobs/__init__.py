import os
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from devobs import views, models

db.create_all()