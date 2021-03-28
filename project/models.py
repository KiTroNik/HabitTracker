from project import db
from flask_login import UserMixin
import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    habits = db.relationship('Habit', backref='user')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Habit(db.Model):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    checked = db.Column(db.Boolean, nullable=False, default=False)
    modify_date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())
    streak = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, checked, modify_date, streak, user_id):
        self.name = name
        self.checked = checked
        self.modify_date = modify_date
        self.streak = streak
        self.user_id = user_id

    def __repr__(self):
        return f'<name {self.name}'
