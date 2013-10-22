from django.contrib.auth.models import Group, User
from django.test import TestCase as DjangoTestCase

from test_utilities import (
    add_user_permissions, Client, TestCase, QuerySetFromIter,
    TestCaseExtensionMixin)


class ClientTest(TestCase):
    def test_login_as(self):
        self.assertFalse(User.objects.exists())
        
        user = self.client.login_as()

        session = self.client.get_session()
        self.assertEqual(session['_auth_user_id'], user.id)
        self.assertTrue(user.username)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('testpassword'))

    def test_login_as_w_user(self):
        existing_user = User.objects.create(is_active=True)
        
        user = self.client.login_as(user=existing_user)

        self.assertIs(user, existing_user)
        session = self.client.get_session()
        self.assertEqual(session['_auth_user_id'], user.id)
        self.assertTrue(user.check_password('testpassword'))

    def test_login_as_w_username(self):
        self.assertFalse(User.objects.exists())
        
        user = self.client.login_as(username='test_user')

        session = self.client.get_session()
        self.assertEqual(session['_auth_user_id'], user.id)
        self.assertEqual(user.username, 'test_user')
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('testpassword'))

    def test_login_as_w_permissions(self):
        user = self.client.login_as(permissions=['auth.change_user'])

        self.assertTrue(user.has_perm('auth.change_user'))
        session = self.client.get_session()
        self.assertEqual(session['_auth_user_id'], user.id)

    def test_login_as_fails(self):
        user = User.objects.create(is_active=False)
        self.assertRaisesMessage(
            AssertionError, 'Can\'t login with user',
            self.client.login_as, user=user)

    def test_get_session(self):
        with self.settings(SESSION_COOKIE_NAME='session_key'):
            session = self.client.get_session()

            self.assertEqual(
                self.client.cookies['session_key'].value, session.session_key)

    def test_get_session_w_existing_session(self):
        with self.settings(SESSION_COOKIE_NAME='session_key'):
            session_key = self.client.get_session().session_key

            session = self.client.get_session()

            self.assertEqual(session.session_key, session_key)
            self.assertEqual(
                self.client.cookies['session_key'].value, session.session_key)


class TestCaseMixinTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/test/get/')

    def test_assert_message_count(self):
        self.assertMessageCount(self.response, 2)

    def test_assert_message_count_fail(self):
        self.assertRaisesMessage(
            AssertionError, 'Message count was 2, expected 1',
            self.assertMessageCount, self.response, 1)

    def test_assert_message_contains(self):
        self.assertMessageContains(self.response, 'test success', 'success')

    def test_assert_message_contains_no_matches(self):
        self.assertRaisesMessage(
            AssertionError,
            'No message contained text "test warning", messages were: "test '
            'success", "test error"',
            self.assertMessageContains, self.response, 'test warning')

    def test_assert_message_contains_multiple_matches(self):
        self.assertRaisesMessage(
            AssertionError,
            'Multiple messages contained text "test": "test success", '
            '"test error"',
            self.assertMessageContains, self.response, 'test')

    def test_assert_message_contains_wrong_log_level(self):
        self.assertRaisesMessage(
            AssertionError,
            'There was one matching message but with different level: '
            'success != error',
            self.assertMessageContains, self.response, 'test success', 'error')

    def test_assert_message_not_contains(self):
        self.assertMessageNotContains(self.response, 'test warning')

    def test_assert_message_not_contains_fails(self):
        self.assertRaisesMessage(
            AssertionError,
            'Message(s) should not contain "test": "test success", '
            '"test error"',
            self.assertMessageNotContains, self.response, 'test')

    def test_assert_not_form_error(self):
        response = self.client.post('/test/post/', {'username': 'jim'})

        self.assertNotFormError(response, 'form', 'username')

    def test_assert_not_form_error_fails(self):
        response = self.client.post('/test/post/')

        self.assertRaisesMessage(
            AssertionError, "[u'This field is required.'] != []",
            self.assertNotFormError, response, 'form', 'username')


class TestCaseTest(TestCase):
    def test_attrs(self):
        self.assertIsInstance(self, TestCaseExtensionMixin)
        self.assertIsInstance(self, DjangoTestCase)
        self.assertEqual(self.client_class, Client)


class AddUserPermissionTest(TestCase):
    def test_add_permission(self):
        user = User.objects.create()

        add_user_permissions(user, ['auth.change_user', 'auth.add_user'])

        self.assertTrue(user.has_perms(['auth.change_user', 'auth.add_user']))


class QuerySetFromIterTest(TestCase):
    def test_qs_from_list(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        users = [user1, user3]

        qs = QuerySetFromIter(users)

        self.assertEqual(len(qs), 2)
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs[0], user1)
        self.assertEqual(qs[1], user3)
        
    def test_empty_qs_from_model(self):
        qs = QuerySetFromIter(model=User)

        self.assertEqual(len(qs), 0)
        self.assertEqual(qs.count(), 0)
        self.assertEqual(qs.model, User)

    def test_missing_list_and_model(self):
        self.assertRaisesMessage(
            ValueError, 'If objects is empty, a model must be included',
            QuerySetFromIter)

    def test_mixed_model_list(self):
        user = User.objects.create(username='user1')
        group = Group.objects.create(name='group1')
        ql = [user, group]

        self.assertRaisesMessage(
            TypeError, 'All objects must be the same model',
            QuerySetFromIter, ql)

    def test_query_qs(self):
        user1 = User.objects.create(username='testuser1')
        user2 = User.objects.create(username='testuser2')
        user3 = User.objects.create(username='otheruser')
        users = [user1, user3]

        qs = QuerySetFromIter(users)

        filter = qs.filter(username__contains='test')
        self.assertSequenceEqual(filter, [user1])
