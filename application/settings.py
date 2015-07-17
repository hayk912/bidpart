# coding=utf-8
# Django settings for application project.
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants
import django
import os
import sys

DEBUG = True
#TEMPLATE_DEBUG = DEBUG
#TEMPLATE_DEBUG = False
TEMPLATE_DEBUG = True
ENVIRONMENT = "production"

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

ADMINS = (
    ('Andreas Karlsson', 'andreas.karlsson@area59.se'),
    ('Johan Frentz', 'johan.frentz@area59.se'),
)

MANAGERS = ADMINS

#DATABASES = {
  #  'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',              # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
 #       'NAME': os.path.join(SITE_ROOT, 'database.sqlite'),  # Or path to database file if using sqlite3.
   #     'USER': '',                                          # Not used with sqlite3.
 #       'PASSWORD': '',                                      # Not used with sqlite3.
  #      'HOST': '',                                          # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    #}
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

BASE_URL = 'bidpart.herokuapp.com'

DEAL_INVOICE_SENDER = ('lennart.sjoblom@bidpart.se', {
    'email': 'lennart.sjoblom@bidpart.se',
    'first_name': 'Lennart',
    'last_name': 'Sjöblom'
})

DEAL_MANUAL_PROCESSING_LIMIT = Decimal('0.7')

LANGUAGES = (
    ('en', _('English')),
    ('sv', _('Swedish'))
)

FLAGS_ROOT = 'core/img/flags/flags-iso/flat/24/'
FLAGS = (
    ('en', 'GB.png'),
    ('sv', 'SE.png')
)

MESSAGE_TAGS = {
    message_constants.DEBUG: 'alert-info',
    message_constants.INFO: 'alert-info',
    message_constants.SUCCESS: 'alert-success',
    message_constants.WARNING: '',
    message_constants.ERROR: 'alert-error'
}

BIDPART_FB_URL = 'https://www.facebook.com/pages/Bidpart-AB/179807262031552'

INTEREST_CONTACT_SENT_TO = 'lennart.sjoblom@bidpart.se'

SHOW_BUY_SELL_DEFAULT = 'all'
SHOW_BUY_SELL = (
    ('all', _('Buy & Sell')),
    ('sell', _('Sell')),
    ('buy', _('Buy'))
)

LOCALE_PATHS = (
    os.path.join(SITE_ROOT, "locale"),
)

SITE_ID = 1

ALLOWED_HOSTS = ['python-bidpart.rhcloud.com']

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Source'],
            ['Format'],
            ['Bold', 'Italic', 'Underline'],
            ['Link', 'Unlink', 'Anchor']
        ],
    },
}

os.environ.get('BASE_IRI', 'localhost')

ADMIN_MEDIA_PREFIX = "/static/admin/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

IMAGE_THUMB_FORMATS = (
    ('admin_thumb', (100, 100, True)),
    ('list_thumb', (78, 48, True)),
    ('ad_thumb', (300, 185, True)),
    ('slider_thumb', (100, 100, True)),
)

IMAGE_THUMB_DEFAULTS = (
    ('list_thumb', 'core/img/default_thumbs/list_thumb.jpg'),
    ('ad_thumb', 'core/img/default_thumbs/ad_thumb.jpg'),
)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'application', 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y_1=0ikcry4(hr6e6a*h3h)%e#or65kxde*cz^gwv^0c9(wvnf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'application.middlewares.CurrencyMiddleware',
    'application.apps.ads.middleware.BuySellMiddleware',
    'application.middlewares.UpdateLocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'currencies.context_processors.currencies',
    'django.core.context_processors.request',
    'application.apps.ads.context_preprocessors.show_buy_cell',
    'application.context_processors.settings',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

AUTHENTICATION_BACKENDS = (
    'application.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'application.apps.accounts.backends.OldPasswordBackend',
    'application.backends.ObjectPermsBackend'
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_OUTPUT_DIR = "cache"
COMPRESS_OFFLINE = True

SENTRY_DSN = 'http://3706426b97cc4833a4466e97c7d84505:c54afaa8ce6a465faa876843d77d15ba@sentry.returngreat.com/4'


ROOT_URLCONF = 'application.urls'

INTERNAL_IPS = ('75.126.24.94',)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'application.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'application', 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',

    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',

    'django_extensions',
    'debug_toolbar',
    'debug_toolbar_user_panel',
    'sendsms',
    'south',
    'compressor',
    'raven.contrib.django',
    'mptt',
    'currencies',
    'django_crontab',
    'autofixture',
    'ckeditor',

    'application.libs.angularjs',
    'application.libs.notifications',

    'application.apps.locale',
    'application.apps.adminsettings',
    'application.apps.ads',
    'application.apps.accounts',
    'application.apps.blog',
    'application.apps.cms',
    'application.apps.contact',
    'application.apps.faq',
    'application.apps.files',
    'application.apps.deals',
    'application.apps.invoice',
    'application.apps.logentryadmin',
    'application.apps.interest',
    'application.apps.edr',
)

GRAPPELLI_INDEX_DASHBOARD = 'application.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Bidpart Admin'

OPENEXCHANGERATES_APP_ID = "873f203c0be044e9ab3186b6cbb69ca7"

# m h  dom mon dow   command
CRONJOBS = [
    ('0 0 * * *', 'application.apps.deals.cron.remind'),
    ('*/15 * * * *', 'application.apps.accounts.cron.update_profile_data')
]

CRONTAB_DJANGO_PROJECT_NAME = "bidpart"

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@bidpart.se'

# EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
# EMAIL_HOST_USER = "AKIAILJZLO6F27RH2LUA"
# EMAIL_HOST_PASSWORD = "Arp+/PVfX7RONlOn/dJPKm2gcGtKa0vRByKStSmT5Utc"

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "workscom"
EMAIL_HOST_PASSWORD = "?workscom?2013"

EMAIL_PORT = 587
EMAIL_USE_TLS = True

BALLOU_SMS_USERNAME = 'Proexcess'
BALLOU_SMS_PASSWORD = 'Jhdkn347'

INVOICE_EXPIRATION_DAYS = 10

# commission levels
#   > eur, percent
COMMISSION_LEVELS = (
    (0, 0.10),
)
AGENT_COMMISSION_LEVELS = (
    (0, 0.25),
    (2500, 0.35),
    (5000, 0.45),
)
MINIMUM_COMMISSION = 60

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': None,
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': False,
    'TAG': 'body',
    'ENABLE_STACKTRACES': True,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar_user_panel.panels.UserPanel',
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    #'application.panels.ProfilingPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from django.template.defaultfilters import slugify

import socket
#hostname = slugify(socket.gethostname()).replace('-', '_')
hostname = 'bidpartherokuappcom'
if os.path.exists(os.path.join(SITE_ROOT, "application/local_settings/%s.py" % hostname)):
    exec("from local_settings.%s import *" % hostname)
else:
    raise Exception("Local settings not found for host %s" % hostname)

exec("from settings_%s import *" % ENVIRONMENT)

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
