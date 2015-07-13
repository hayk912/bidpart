DEBUG = True
STATIC_URL = "http://static.stage.bidpart.com/"
MEDIA_URL = "http://media.stage.bidpart.com/"
ADMIN_MEDIA_PREFIX = "/admin/"
COMPRESS_ENABLED = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SENDSMS_BACKEND = 'application.backends.BallouSMSBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# SENDSMS_BACKEND = 'sendsms.backends.locmem.SmsBackend'
SITE_URL = 'http://stage.bidpart.com'

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
