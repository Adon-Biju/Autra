# Development settings (your local computer)

from .base import *  # Import everything from base.py
from decouple import config

DEBUG = True  # Show detailed error pages

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# PostgreSQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='autra_db'),
        'USER': config('DB_USER', default='autra_user'),
        'PASSWORD': config('DB_PASSWORD', default='autra123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Print emails to console instead of sending real emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'