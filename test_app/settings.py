
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
ROOT_URLCONF = 'test_app.urls'
SECRET_KEY = 'keepitsecretkeepitsafe'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_nose',
    'test_app',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ('--nocapture', )
