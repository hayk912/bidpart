STATIC_URL = "http://blooming-peak-2351.herokuapp.com/"
MEDIA_ROOT = "/mnt/cdn/bidpart-django/media/"
MEDIA_URL = "blooming-peak-2351.herokuapp.com"
ADMIN_MEDIA_PREFIX = "/admin/"
COMPRESS_ENABLED = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SENDSMS_BACKEND = 'application.backends.BallouSMSBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# SENDSMS_BACKEND = 'sendsms.backends.locmem.SmsBackend'
SITE_URL = 'blooming-peak-2351.herokuapp.com'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '192.168.192.143:11211',
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
