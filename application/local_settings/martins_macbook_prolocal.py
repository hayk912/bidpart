ENVIRONMENT = "development"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',                # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bidpart-2.0',                            # Or path to database file if using sqlite3.
        'USER': 'root',                                          # Not used with sqlite3.
        'PASSWORD': 'Mtm3w2DJ',                                      # Not used with sqlite3.
        'HOST': '127.0.0.1',                                          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    }
}

INTEREST_CONTACT_SENT_TO = 'martin@workscom.se'

