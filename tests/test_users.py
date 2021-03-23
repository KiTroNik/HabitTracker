import os
import tempfile
import pytest
from project import app, db, bcrypt
from project.models import User
from config import TestingConfig


@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()


class TestUser:
    def test_login_page_shows(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Please log in to access your habits' in response.data
