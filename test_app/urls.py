from django.conf.urls import patterns

from test_app.views import get_test, post_test 


urlpatterns = patterns(
    '',
    (r'^test/get/$', get_test),
    (r'^test/post/$', post_test),
)

