from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from functools import wraps


users_blueprint = Blueprint('users', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function


@users_blueprint.route('/')
def login():
    return render_template('users/login.html')


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    return "CHUJ"


@users_blueprint.route('/logout/')
@login_required
def logout():
    return "CHUJ"
