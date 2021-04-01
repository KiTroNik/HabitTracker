from .utils import *
from freezegun import freeze_time
from datetime import date, timedelta


class TestHabit:
    def test_unlogged_users_cant_go_to_habit_page(self, client):
        response = client.get('/habits/')
        assert b'Your habits' not in response.data

    def test_logged_users_can_go_to_habit_page(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/habits/')
        assert b'Your habits' in response.data

    def test_if_there_is_no_habits_comment_is_visible(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = client.get('/habits/')
        assert b'There is no habits. Come back tommorow or add a habit.' in response.data

    def test_if_there_are_habits_comment_is_not_visible(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        response = client.get('/habits/')
        assert b'There is no habits. Come back tommorow or add a habit.' not in response.data

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
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        logout(client)
        response = client.get('/delete/1', follow_redirects=True)
        assert b'We hope this habit will stay in your life forever.' not in response.data

    def test_logged_users_can_delete_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        response = client.get('/delete/1', follow_redirects=True)
        assert b'We hope this habit will stay in your life forever.' in response.data

    def test_unlogged_users_cant_check_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        logout(client)
        response = client.get('/check/1', follow_redirects=True)
        assert b'Keep it up!' not in response.data

    def test_logged_users_can_check_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        response = client.get('/check/1', follow_redirects=True)
        assert b'Keep it up!' in response.data

    def test_logged_users_see_own_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        response = create_habit(client, 'some habit')
        assert b'some habit' in response.data

    def test_logged_users_dont_see_others_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        logout(client)
        register(client, 'Wojciech', 'suchodolski@wp.pl', 'szkolna17', 'szkolna17')
        response = login(client, 'Wojciech', 'szkolna17')
        assert b'some habit' not in response.data

    def test_user_can_delete_only_own_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        logout(client)
        register(client, 'Wojciech', 'suchodolski@wp.pl', 'szkolna17', 'szkolna17')
        login(client, 'Wojciech', 'szkolna17')
        response = client.get('/delete/1', follow_redirects=True)
        assert b'We hope this habit will stay in your life forever.' not in response.data

    def test_user_can_check_only_own_habits(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        logout(client)
        register(client, 'Wojciech', 'suchodolski@wp.pl', 'szkolna17', 'szkolna17')
        login(client, 'Wojciech', 'szkolna17')
        response = client.get('/check/1', follow_redirects=True)
        assert b'Keep it up!' not in response.data

    def test_habit_can_be_checked_only_once_a_day(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        response = client.get('/check/1', follow_redirects=True)
        assert b'Check!' not in response.data

    def test_habit_streak_is_incrementing(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        response = client.get('/check/1', follow_redirects=True)
        assert b'Streak: 1' in response.data

    def test_habit_is_uncheked_every_day(self, client):
        register(client, 'John', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'John', 'mysecret')
        create_habit(client, 'some habit')
        client.get('/check/1', follow_redirects=True)
        with freeze_time(date.today() + timedelta(days=1)):
            response = client.get('/habits/', follow_redirects=True)
            assert b'Check!' in response.data

    def test_habit_streak_is_reseted_after_more_than_one_day_user_unchecked(self, client):
        register(client, 'Johnn', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'Johnn', 'mysecret')
        create_habit(client, 'some habit')
        client.get('/check/1', follow_redirects=True)
        with freeze_time(date.today() + timedelta(days=3)):
            client.get('/habits/', follow_redirects=True)
            response = client.get('/check/1', follow_redirects=True)
            assert b'Streak: 1' in response.data

    def test_habit_streak_is_not_reseted_after_one_day_user_unchecked(self, client):
        register(client, 'Johnn', 'johndoe@wp.pl', 'mysecret', 'mysecret')
        login(client, 'Johnn', 'mysecret')
        create_habit(client, 'some habit')
        client.get('/check/1', follow_redirects=True)
        with freeze_time(date.today() + timedelta(days=1)):
            client.get('/habits/', follow_redirects=True)
            response = client.get('/check/1', follow_redirects=True)
            assert b'Streak: 2' in response.data
