from flask import Blueprint, render_template, redirect, url_for, session, flash
from functools import wraps
from .forms import LoginForm, RegisterForm

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
    form = LoginForm()
    return render_template('users/login.html', form=form)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('users/register.html', form=form)


@users_blueprint.route('/logout/')
@login_required
def logout():
    return "CHUJ"
