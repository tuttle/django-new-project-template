########################################################################
# This module contains project-specific customizations.
########################################################################

# DRY: Build on the Django's project_template settings.
from .base_settings import *  # @UnusedWildImport

########################################################################
# SETTINGS COMMON FOR ALL INSTALLATIONS (production, staging, development)
########################################################################

# Note: Must be a safe Python identifier
PROJECT_IDENT = 'myproject'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROJECT_IDENT,
        'USER': PROJECT_IDENT,
        'PASSWORD': 'will be set in the installation-specific (local) settings',
        'HOST': '',  # PostgreSQL, an empty string means to use a Unix domain socket for the connection
    }
}

# Must be set later in the installation-specific (local) settings.
SECRET_KEY = None

DEVELOPER = ('Vlada Macek (%s developer)' % PROJECT_IDENT, 'macek@sandbox.cz')
DEVELOPER_EMAIL = '%s <%s>' % DEVELOPER

# Contacts to the technical app administrators.
ADMINS = (DEVELOPER,)

TIME_ZONE = 'Europe/Prague'

# TODO: No timezone support for now, Postgres gives us no
# need for data migration when turned on later.
USE_TZ = False

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_IDENT
ROOT_URLCONF = '%s.urls' % PROJECT_IDENT

# STATIC_ROOT: We are not using it; the production webserver is expected
# to serve the static files directly from the apps dirs.

STATIC_URL = '/s/'
MEDIA_URL = '/media/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'django_extensions',
    'south',
    'useful.django',

    'myproject.apps.core',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'useful.django.cached_auth.CachedAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Automatic "load" of new features. Could be removed on Django 1.5.
import django.template
django.template.add_to_builtins('django.templatetags.future')

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
#    'myproject.context_processors.myproject',
)

# Available languages:
# https://docs.djangoproject.com/en/1.3/ref/settings/#languages
_ = lambda s: s
LANGUAGES = (
    ('en', _('English')),
    ('cs', _('Czech')),
)

LOCALE_MAP = {
    'en': 'en_US.UTF-8',
    'cs': 'cs_CZ.UTF-8',
#    'fr': 'fr_FR.UTF-8',
#    'de': 'de_DE.UTF-8',
#    'pl': 'pl_PL.UTF-8',
#    'da': 'da_DK.UTF-8',
}

import os.path as p

# Directory of manage.py
PROJECT_ROOT = p.dirname(p.dirname(p.abspath(__file__)))

# Without this the following is issued:
# DeprecationWarning: Translations in the project directory aren't supported
# anymore. Use the LOCALE_PATHS setting instead.
LOCALE_PATHS = (p.join(PROJECT_ROOT, 'locale'),)

del p

# Where to redirect after login when the login view gets no 'next' parameter.
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'

# The # of days users will have to activate their accounts after registering.
ACCOUNT_ACTIVATION_DAYS = 7

#AUTH_PROFILE_MODULE = 'some-app.UserProfile'

#AUTHENTICATION_BACKENDS = ('useful.django.auth.EmailLoginModelBackend',)

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        'TIMEOUT': 60*60*24*7,
#        'KEY_PREFIX': PROJECT_IDENT,
#    }
#}

#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

INTERNAL_IPS = ('127.0.0.1',)

########################################################################
# SETTINGS VARYING PER INSTALLATION (production, staging, development)
########################################################################

INSTALLATIONS = {
    'production': dict(
        SITE_ID = 1,
        HTTP_PORT = 80,  # Not a Django setting, port number for constructing links

        DEBUG = False,
        TEMPLATE_DEBUG = False,

        MEDIA_ROOT = '/var/www/%s/' % PROJECT_IDENT,

        EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_IDENT,
        MANAGERS = ADMINS,   # + ('other non-tech client staff contact', ...)

        # Not a Django setting! Where the application e-mails should be diverted
        # instead of being sent to real recipients. Uses the same format as ADMINS.
        DIVERT_EMAILS_TO = None,

        DEFAULT_FROM_EMAIL = 'to be set',
        SERVER_EMAIL = 'to be set',
    ),

    'staging': dict(
        SITE_ID = 2,
        HTTP_PORT = 80,

        DEBUG = False,
        TEMPLATE_DEBUG = False,

        MEDIA_ROOT = '/var/www/%s.staging/' % PROJECT_IDENT,

        EMAIL_SUBJECT_PREFIX = '[%s.staging] ' % PROJECT_IDENT,
        MANAGERS = ADMINS,
        DIVERT_EMAILS_TO = ADMINS,

        DEFAULT_FROM_EMAIL = 'to be set',
        SERVER_EMAIL = 'to be set',
    ),

    'devel': dict(
        SITE_ID = 3,
        HTTP_PORT = 8000,

        DEBUG = True,
        TEMPLATE_DEBUG = True,

        MEDIA_ROOT = '/home/tuttle/tmp/django-media/myproject/',

        EMAIL_SUBJECT_PREFIX = '[%s.devel] ' % PROJECT_IDENT,
        MANAGERS = ADMINS,
        DIVERT_EMAILS_TO = ADMINS,

        DEFAULT_FROM_EMAIL = DEVELOPER_EMAIL,
        SERVER_EMAIL = DEVELOPER_EMAIL,
    ),
}
