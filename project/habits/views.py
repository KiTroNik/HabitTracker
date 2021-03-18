from flask import Blueprint, render_template

habits_blueprint = Blueprint('habits', __name__)


@habits_blueprint.route('/habits/')
def habits():
    return render_template('habits/habits.html')
