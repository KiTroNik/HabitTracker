from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import NewHabitForm
from project.models import Habit
from project import db
from flask_login import login_required, current_user
from datetime import date, timedelta

habits_blueprint = Blueprint('habits', __name__)


def redefine_habits():
    Habit.query.filter(Habit.modify_date == date.today() - timedelta(days=1)) \
        .filter(Habit.user_id == current_user.id).update(
        {Habit.checked: False, Habit.modify_date: date.today()}
    )

    Habit.query.filter((Habit.modify_date != date.today() - timedelta(days=1)) and Habit.modify_date != date.today())\
        .filter(Habit.user_id == current_user.id).update(
        {Habit.checked: False, Habit.modify_date: date.today(), Habit.streak: 0}
    )

    db.session.commit()


def checked_habits():
    return Habit.query.filter_by(user_id=current_user.id).filter_by(checked=True)


def unchecked_habits():
    return Habit.query.filter_by(user_id=current_user.id).filter_by(checked=False)


@habits_blueprint.route('/habits/')
@login_required
def habits():
    redefine_habits()
    return render_template(
        'habits/habits.html',
        checked_habits=checked_habits(),
        unchecked_habits=unchecked_habits()
    )


@habits_blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
def add_habit():
    form = NewHabitForm()
    if request.method == 'POST' and form.validate():
        new_habit = Habit(
            form.name_of_habit.data,
            False,
            date.today(),
            0,
            current_user.id
        )
        db.session.add(new_habit)
        db.session.commit()
        flash('New habit created successfully')
        return redirect(url_for('habits.habits'))
    return render_template('habits/new.html', form=form)


@habits_blueprint.route('/check/<int:habit_id>/')
@login_required
def check(habit_id):
    habit = Habit.query.filter_by(id=habit_id)
    if current_user.id == habit.first().user_id:
        habit.update({'checked': True, 'modify_date': date.today(), 'streak': habit.first().streak + 1})
        db.session.commit()
        flash("Keep it up!")
    else:
        flash("Operation denied")
    return redirect(url_for('habits.habits'))


@habits_blueprint.route('/delete/<int:habit_id>')
@login_required
def delete(habit_id):
    habit = Habit.query.filter_by(id=habit_id)
    if current_user.id == habit.first().user_id:
        habit.delete()
        db.session.commit()
        flash('We hope this habit will stay in your life forever.')
    else:
        flash('Operation denied')
    return redirect(url_for('habits.habits'))
