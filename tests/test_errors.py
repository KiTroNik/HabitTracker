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


class TestErrors:
    def test_setup(self, client):
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Please log in to access your habits' in response.data

    def test_404_error_renders_proper(self, client):
        response = client.get('/not_exists', follow_redirects=True)
        assert response.status_code == 404
        assert b'What you were looking for is just not there.' in response.data
