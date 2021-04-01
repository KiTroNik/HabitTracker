from .utils import *


@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()


class TestMain:
    def test_home_page_shows(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Habit Tracker' in response.data

    def test_404_error_renders_proper(self, client):
        response = client.get('/not_exists', follow_redirects=True)
        assert response.status_code == 404
        assert b'What you were looking for is just not here.' in response.data

    def test_home_page_if_user_logged_off(self, client):
        response = client.get('/', follow_redirects=True)
        assert b'Login' in response.data
        assert b'Signup' in response.data

    def test_navbar_if_user_logged_off(self, client):
        response = client.get('/', follow_redirects=True)
        assert b'Home' in response.data

    def test_home_page_changes_if_user_logged(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/', follow_redirects=True)
        assert b'Login' not in response.data
        assert b'Signup' not in response.data
        assert b'Logout' in response.data

    def test_navbar_changes_if_user_logged(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/', follow_redirects=True)
        assert b'Habits' in response.data
