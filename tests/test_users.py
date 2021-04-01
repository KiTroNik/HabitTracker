from .utils import *


class TestUser:
    def test_login_page_shows(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert b'Remember me' in response.data

    def test_login_form_validates_input(self, client):
        response = login(client, 'foo', 'bar')
        assert b'Field must be between 4 and 40 characters long.' in response.data
        response = client.post('/login/', data=dict(username='', password='siema'), follow_redirects=True)
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
        assert b'Signup' in response.data

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

    def test_string_representation_of_user(self, client):
        db.session.add(User(
            'Johnny',
            'john@doe.com',
            'secret'
        ))
        db.session.commit()
        user = User.query.filter_by(username='Johnny').first()
        assert user.__repr__() == "<User 'Johnny'>"

    def test_user_cant_login_again_if_logged(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/login/', follow_redirects=True)
        assert b'Login' not in response.data

    def test_user_cant_register_if_logged(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        assert b'Thank you for registering. Please log in.' not in response.data
