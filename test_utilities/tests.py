#from django.core.exceptions import ValidationError
#from test_utilities import TestCase


#class TestCaseTest(TestCase):
#    def raise_error(self, error_message, exc=ValidationError):
#        raise exc(error_message)

#    def test_raises_message_return_message(self):
#        self.assertRaisesMessage(
#            Exception, self.raise_error, 'test message',
#            error_message='test message', exc=Exception)

#    def test_raises_message_return_messages_list(self):
#        self.assertRaisesMessage(
#            ValidationError, self.raise_error, ['test message1', 'message2'],
#            error_message=['test message1', 'message2'])

#    def test_raises_message_return_message_dict(self):
#        self.assertRaisesMessage(
#            ValidationError, self.raise_error, {'field': 'test message1'},
#            error_message={'field': 'test message1'})

#    def test_raises_message_messages_dont_match(self):
#        # Assert that assertRaisesMessage raises AssertionError when messages
#        # don't match
#        self.assertRaises(
#            AssertionError,
#            self.assertRaisesMessage, ValidationError, self.raise_error,
#            ['test message1'], error_message=['message2'])

#    def test_raises_message_specified_exception_not_raised(self):
#        # Assert that assertRaisesMessage raises AssertionError when sprcified
#        # exception is not raised
#        self.assertRaisesMessage(
#            AssertionError,
#            self.assertRaisesMessage, 'ValidationError not raised',
#            ValidationError, str, 'test message')
