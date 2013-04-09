from django.conf import settings
from django.contrib.messages import DEFAULT_TAGS
from django.test import TestCase as DjangoTestCase
from django.utils.importlib import import_module


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
    pass
