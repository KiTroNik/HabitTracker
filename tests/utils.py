import pytest
from project import app, db, bcrypt
from project.models import User, Habit
from config import TestingConfig
from datetime import date


@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()


def login(client, username, password):
    return client.post('/login/', data=dict(username=username, password=password), follow_redirects=True)


def register(client, username, email, password, confirm):
    return client.post('/register/', data=dict(
        username=username,
        email=email,
        password=password,
        confirm=confirm
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout/', follow_redirects=True)


def create_user(username, email, password):
    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()


def create_habit(client, name):
    return client.post('/add/', data=dict(
        name_of_habit=name,
    ), follow_redirects=True)
