from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
from project.models import User
from project import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, login_user, logout_user

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    remember = True if form.remember_me.data else False
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=remember)
            flash('Welcome!')
            return redirect(url_for('habits.habits'))
        else:
            flash('Invalid username or password')
    return render_template('users/login.html', form=form)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        new_user = User(
            form.username.data,
            form.email.data,
            bcrypt.generate_password_hash(form.password.data)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thank you for registering. Please log in.')
            return redirect(url_for('users.login'))
        except IntegrityError:
            flash('That username and/or email already exist.')
            return render_template('users/register.html', form=form)
    return render_template('users/register.html', form=form)


@users_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('home_page'))
