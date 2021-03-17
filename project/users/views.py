from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/')
def login():
    return render_template('users/login.html')
