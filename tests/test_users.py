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


def login(client, username, password):
    return client.post('/', data=dict(username=username, password=password), follow_redirects=True)


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


class TestUser:
    def test_login_page_shows(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Please log in to access your habits' in response.data

    def test_login_form_validates_input(self, client):
        response = login(client, 'foo', 'bar')
        assert b'Field must be between 4 and 40 characters long.' in response.data
        response = client.post('/', data=dict(username='', password='siema'), follow_redirects=True)
        assert b'This field is required.' in response.data

    def test_unregistered_user_cant_login(self, client):
        response = login(client, 'John', 'secret')
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data

    def test_user_can_login(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        response = login(client, 'John', 'mysecret')
        assert b'Welcome' in response.data

    def test_invalid_login_data(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        response = login(client, 'John', 'dupa')
        assert b'Invalid username or password' in response.data

    def test_register_page_shows(self, client):
        response = client.get('/register/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Already registered?' in response.data

    def test_user_can_register(self, client):
        response = register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        assert b'Thank you for registering. Please log in.' in response.data

    def test_is_is_impossible_to_add_two_identical_users(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        response = register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        assert b'That username and/or email already exist.' in response.data

    def test_logged_users_can_logout(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = logout(client)
        assert b'Goodbye.' in response.data

    def test_not_logged_users_cant_logout(self, client):
        response = logout(client)
        assert b'Goodbye.' not in response.data
