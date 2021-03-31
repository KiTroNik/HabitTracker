from .utils import *


class TestHabit:
    def test_unlogged_users_cant_go_to_habit_page(self, client):
        response = client.get('/habits/')
        assert b'Your habits' not in response.data

    def test_logged_users_can_go_to_habit_page(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/habits/')
        assert b'Your habits' in response.data

    def test_unlogged_users_cant_see_create_habit_form(self, client):
        response = client.get('/add/')
        assert b'Add habit' not in response.data

    def test_logged_in_users_can_see_create_habit_form(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/add/')
        assert b'Add habit' in response.data

    def test_unlogged_users_cant_create_habits(self, client):
        response = create_habit(client, 'some habit')
        assert b'New habit created successfully' not in response.data

    def test_logged_users_can_create_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = create_habit(client, 'some habit')
        assert b'New habit created successfully' in response.data

    def test_unlogged_users_cant_delete_habits(self, client):
        pass

    def test_logged_users_can_delete_habits(self, client):
        pass

    def test_unlogged_users_cant_check_habits(self, client):
        pass

    def test_logged_users_can_check_habits(self, client):
        pass

    def test_logged_users_see_only_own_habits(self, client):
        pass

    def test_user_can_delete_only_own_habits(self, client):
        pass

    def test_user_can_check_only_own_habits(self, client):
        pass

    def test_habit_can_be_checked_only_once_a_day(self, client):
        pass

    def test_habit_streak_is_incrementing(self, client):
        pass

    def test_habit_is_uncheked_every_day(self, client):
        pass

    def test_habit_streak_is_reseted_after_more_than_one_day_user_unchecked(self, client):
        pass
