import pytest
from project import app, db, bcrypt
from project.models import User, Habit
from config import TestingConfig


@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()


class TestHabit:
    pass
