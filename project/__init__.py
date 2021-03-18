from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.habits.views import habits_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(habits_blueprint)
