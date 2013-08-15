import random
import string

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.messages import DEFAULT_TAGS
from django.db.models.query import QuerySet
from django.test import Client as DjangoClient, TestCase as DjangoTestCase
from django.utils.importlib import import_module


class Client(DjangoClient):
    def login_as(self, user=None, username='', password='testpassword',
                 permissions=None, *args, **kwargs):
        if not user:
            if not username:
                username = ''.join(random.choice(
                    string.ascii_letters + string.digits)
                    for i in xrange(random.randint(6, 20)))
            user = User.objects.create(
                username=username, is_active=True, *args, **kwargs)

        user.set_password(password)
        user.save()

        if permissions:
            add_user_permissions(user, permissions)

        assert (self.login(username=user.username, password=password),
                'Can\'t login with user')

        return user


class TestCaseExtensionMixin(object):
    def assertMessageCount(self, response, expect_num):
        """
        Asserts that exactly the given number of messages have been sent.
        """

        actual_num = len(response.context['messages'])
        if actual_num != expect_num:
            self.fail('Message count was %d, expected %d' % (
                actual_num, expect_num))

    def assertMessageContains(self, response, text, level=None):
        """
        Asserts that there is exactly one message containing the given text.
        """

        messages = response.context['messages']

        matches = [m for m in messages if text in m.message]

        if len(matches) == 1:
            msg = matches[0]
            if (level is not None and msg.level != level and
                    DEFAULT_TAGS[msg.level] != level):
                msg_level_txt = DEFAULT_TAGS.get(msg.level, 'NO LEVEL')
                expected_level = DEFAULT_TAGS.get(level, level)
                self.fail('There was one matching message but with different '
                          'level: %s != %s' % (msg_level_txt, expected_level))
            self.assertContains(response, text)
            return

        elif len(matches) == 0:
            messages_str = ", ".join('"%s"' % m for m in messages)
            self.fail('No message contained text "%s", messages were: %s' % (
                text, messages_str))
        else:
            self.fail('Multiple messages contained text "%s": %s' % (
                text, ", ".join(('"%s"' % m) for m in matches)))

    def assertMessageNotContains(self, response, text):
        """ Assert that no message contains the given text. """

        messages = response.context['messages']

        matches = [m for m in messages if text in m.message]

        if len(matches) > 0:
            self.fail('Message(s) should not contain "%s": %s' % (
                text, ", ".join(('"%s"' % m) for m in matches)))

    def assertNotFormError(self, response, form, field):
        self.assertEqual(response.context[form][field].errors, [])

    def get_session(self):
        engine = import_module(settings.SESSION_ENGINE)
        if hasattr(self.client.session, 'session_key'):
            store = engine.SessionStore(self.client.session.session_key)
        else:
            store = engine.SessionStore()
        store.save()  # we need to make load() work, or the cookie is worthless
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        return self.client.session


class TestCase(TestCaseExtensionMixin, DjangoTestCase):
    client = Client


class QuerySetFromIter(QuerySet):
    """
    Creates a QuerySet from an iterable of Django objects, which can then be
    used like a normal QuerySet.
    """
    def __init__(self, objects=[], model=None, query=None, *args, **kwargs):
        if model is None:
            if len(objects):
                model = type(objects[0])
            else:
                # TODO: find a better way to handle this
                raise ValueError(
                    'If objects is empty, a model must be included')

        pk_list = []
        for r in objects:
            if not type(r) is model:
                raise TypeError('All objects must be the same model')
            pk_list.append(r.pk)
        super(QuerySetFromIter, self).__init__(model, query, *args, **kwargs)
        self._result_cache = list(objects)
        self.query.add_filter(('pk__in', pk_list))

    def _clone(self, klass=None, setup=False, **kwargs):
        if klass is None:
            klass = self.__class__.__base__
        return super(QuerySetFromIter, self)._clone(klass, setup, **kwargs)


def add_user_permissions(user, permissions=[]):
    """
    Utility to give a user permissions easily

    Usage:
    add_user_permissions(user, ['app_label.code_name', ...])
    """
    for permission_name in permissions:
        app_label, codename = permission_name.split('.')
        permission = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename)
        user.user_permissions.add(permission)
    return user
