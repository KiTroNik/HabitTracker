from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class NewHabitForm(FlaskForm):
    name_of_habit = StringField('Habit', [DataRequired(), Length(max=50)])