Django Test Utilities
======================

Django Test Utilities is a small suite which brings additional useful
funcationality to testing Django applications


Installation
------------
Install with pip from pypi:

    pip install django-test-utilities

Or from github:

    pip install git+https://github.com/jsatt/django-test-utilities.git


TestCase and TestCaseExtensionMixin
-----------------------------------
The simplest way to get started is to extend the Test Utilities TestCase when
writing your own tests

    from test_utilities import TestCase

    class SampleTest(TestCase):
        def setUp(self):
        ...
        ...
        ...

TestCase extends TestCaseExtensionMixin, the default Django TestCase and uses
the provided test Client.

TestCaseExtensionMixin provides few new assertion methods and a method for
getting a reusable Django session.

#### .assertMessageCount(response, expect_num) ####

Asserts that the `response` context contains exactly `expect_num` messages.

    ...
    self.assertMessageCount(response, 3)
    ...

#### .assertMessageContains(response, text[, level]) ####

Asserts that the `response` context contains at lease one message
containing `text`. Failure output contains a list of actual messages in the
context. `level` can optionally be one of `'success'`, `'error'`, `'info'`,
`'warning'`, or `'debug'` to confirm that any messages found are of the
correct log level, with a failure indicating the log level of the match.
Multiple matches will also raise a failure as indicator that you may not be
checking for specific enough text, which could result in false positives
otherwise.

    ...
    self.assertMessageContains
    self.assertMessageContains(response, 'completed successfully', 'success')
    ...

#### .assertMessageNotContains(response, text) ####

As the opposite of assertMessageContains, this asserts that the `response`
does not contain any messages containing the specified `text`.

    ...
    self.assertMessageNotContains(response, 'failed to submit')
    ...

#### .assertNotFormError(response, form, field) ####

Django provides assertFormError. This asserts that `response` doesn't
contains any errors on the field of the form specified.

    ...
    self.assertNotFormError(response, 'signup_form', 'address1')
    ...


Client
------

#### .login_as([user], [username], [password], [permissions], args, kwargs) ####

This is a shortcut to create an active django user and logging that user in
to the client. If an existing `user` is provided, that user is logged in,
otherwise a new user object is created using the `username`, `password`,
and all remaining `args` and `kwargs` provided being passed directly to the
User model.  A list of Django `permissions` can also be provided in the
format 'app_name.code_name'. The user that is created is returned, or an
assertion is raised it the user cannot be logged in.

    ...
    self.client.login_as(
        username='bob', email='test@email.com', is_staff=True,
        permissions=['auth.change_user', 'my_app.add_example'])
    ...

#### .get_session() ####

Setting and checking session values with Django test clients is sometimes a
pain. This will get the current client session, or create it if it doesn't
exist. You can then set session attributes and assert their values.

    ...
    session = self.client.get_session()
    session['pages_viewed'] = 5
    session.save()

    # Get a view that modifies the session
    response = self.client.get('/example_page/')

    self.assertEqual(session['pages_viewed'], 6)
    ...


Other Utilities
---------------

#### QuerySetFromIter([objects], [model], args, kwargs) ####

This is a utility for generating a queryset from an interator, most
commonly helpful when using tool like model_mommy to generate model
instances. Providing a list or tuple of `objects` will create a queryset of
those objects in that order and insure that any further queryset
manipulations will be executed against only those items. If a model is not
provided, it will be detected from the first item. All items *must* be
instances of the same Model.

    ...
    magazines = [self.mag1, self.mag3, self.mag2]
    mqs = QuerySetFromIter(magazines, Magazine)
    mqs.order_by('publish_date')

    books = mommy.make('my_app.Book', author='Jimmy Joe', _quantity=3)
    bqs = QuerySetFromIter(books)
    bqs.filter(year=2012)
    ...


#### add_user_permissions(user, permissions) ####

Django doesn't have a quick way to setup permissions on existing users.
This function looks up the `permissions` provied and adds all of them to
the user provided.

    ...
    add_user_permissions(
        user1, permissions=['auth.change_user', 'my_app.add_example'])
    ...


License
-------

Copyright 2013 Jeremy Satterfield

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
