from flask import Blueprint, render_template, redirect, url_for, flash, request
from project.models import Habit
from project import db
from flask_login import login_required, current_user
from datetime import date, timedelta

habits_blueprint = Blueprint('habits', __name__)


def redefine_habits():
    Habit.query.filter((Habit.modify_date + timedelta(days=1)) == date.today()).update(
        {Habit.checked: False, Habit.modify_date: date.today()}
    )
    Habit.query.filter((Habit.modify_date + timedelta(days=1)) < date.today()).update(
        {Habit.checked: False, Habit.modify_date: date.today(), Habit.streak: 0}
    )
    db.session.commit()


@habits_blueprint.route('/habits/')
@login_required
def habits():
    redefine_habits()
    return render_template('habits/habits.html')
