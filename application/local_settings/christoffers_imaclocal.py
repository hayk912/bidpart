from application.settings import SITE_ROOT
import os

ENVIRONMENT = "development"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',                # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bidpart-django',                            # Or path to database file if using sqlite3.
        'USER': 'root',                                          # Not used with sqlite3.
        'PASSWORD': '',                                      # Not used with sqlite3.
        'HOST': '127.0.0.1',                                          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    },
    'empty': {
        'ENGINE': 'django.db.backends.sqlite3',              # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'empty.sqlite'),  # Or path to database file if using sqlite3.
        'USER': '',                                          # Not used with sqlite3.
        'PASSWORD': '',                                      # Not used with sqlite3.
        'HOST': '',                                          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    },
    'testimport': {
        'ENGINE': 'django.db.backends.sqlite3',              # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'testimport.sqlite'),  # Or path to database file if using sqlite3.
        'USER': '',                                          # Not used with sqlite3.
        'PASSWORD': '',                                      # Not used with sqlite3.
        'HOST': '',                                          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    },
}

DEBUG = False
