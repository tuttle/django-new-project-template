########################################################################
# This is an installation-specific (local) settings module.
########################################################################

from myproject.conf.project_settings import *  # @UnusedWildImport

INSTALLATION_TYPE = 'devel'

globals().update(INSTALLATIONS[INSTALLATION_TYPE])

# NEVER, NEVER store real production/staging passwords in the repository!
DATABASES['default']['PASSWORD'] = 'installation database password'

# Generate an installation-specific secret key, crucial for production/staging
SECRET_KEY = 'installation secret key'

#MEDIA_ROOT = '/some/path/if/necessary/...'

#EMAIL_HOST = '10.201.0.1'

if INSTALLATION_TYPE != 'devel':
    # Make all templates to be cached in memory. Server will need to be reloaded on template change.
    TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),)

import os

if (SITE_ID > 1) and os.getenv('DDT'):
    print "Enabling django-debug-toolbar..."

    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) \
                       + MIDDLEWARE_CLASSES

    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
