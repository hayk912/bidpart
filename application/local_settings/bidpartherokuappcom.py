ENVIRONMENT = "production"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',                # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bidpart_django',                            # Or path to database file if using sqlite3.
        'USER': 'litonkhan',                                 # Not used with sqlite3.
        'PASSWORD': '55femtiofem654',                           # Not used with sqlite3.
        'HOST': 'web389.webfaction.com',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    }
}

COMPRESS_OFFLINE = False
