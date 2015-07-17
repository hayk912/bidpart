ENVIRONMENT = "production"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',                # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'python',                            # Or path to database file if using sqlite3.
        'USER': 'adminmLI8wna',                                 # Not used with sqlite3.
        'PASSWORD': 'hNQHrq6UzscH',                           # Not used with sqlite3.
        'HOST': '75.126.24.94',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    }
}



COMPRESS_OFFLINE = False
