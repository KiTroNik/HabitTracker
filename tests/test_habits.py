from .utils import *


class TestHabit:
    def test_unlogged_users_cant_go_to_habit_page(self, client):
        response = client.get('/habits/')
        assert b'Your habits' not in response.data

    def logged_users_can_go_to_habit_page(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
