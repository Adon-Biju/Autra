# Development settings (your local computer)

from .base import *  # Import everything from base.py

DEBUG = True  # Show detailed error pages

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use simple SQLite database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Print emails to console instead of sending real emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'