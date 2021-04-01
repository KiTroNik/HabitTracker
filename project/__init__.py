from flask import Flask, render_template
from config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(ProductionConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from project.users.views import users_blueprint
from project.habits.views import habits_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(habits_blueprint)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500
