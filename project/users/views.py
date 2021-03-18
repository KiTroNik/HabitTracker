from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from functools import wraps
from .forms import LoginForm, RegisterForm
from project.models import User
from project import bcrypt, db
from sqlalchemy.exc import IntegrityError

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
    if request.method == 'POST' and form.validate():
        user = User(
            form.username.data,
            form.email.data,
            bcrypt.generate_password_hash(form.password.data)
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Thank you for registering')
            return redirect(url_for('users.login'))
        except IntegrityError:
            flash('That username and/or email already exist.')
            return render_template('users/register.html', form=form)
    return render_template('users/register.html', form=form)


@users_blueprint.route('/logout/')
@login_required
def logout():
    return "CHUJ"
