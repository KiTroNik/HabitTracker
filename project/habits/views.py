from flask import Blueprint, render_template
from flask_login import login_required

habits_blueprint = Blueprint('habits', __name__)


@habits_blueprint.route('/habits/')
@login_required
def habits():
    return render_template('habits/habits.html')
