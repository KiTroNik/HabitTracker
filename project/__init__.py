from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint)
