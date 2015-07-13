DEBUG = True
COMPRESS_ENABLED = True
EMAIL_BACKEND = 'application.backends.RedirectEmailBackend'
SENDSMS_BACKEND = 'sendsms.backends.locmem.SmsBackend'
SITE_URL = '75.126.24.94'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
