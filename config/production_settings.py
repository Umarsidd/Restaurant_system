"""
Production settings for deployment
"""
from .settings import *
import os
import dj_database_url

# SECURITY
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
ALLOWED_HOSTS = [
    'restaurant-system-jtqy.onrender.com',  # Specific Render domain
    '*.onrender.com',  # Wildcard for all Render domains
    '.onrender.com',   # Subdomain wildcard
    '.railway.app', 
    '.pythonanywhere.com',
    'localhost',
    '127.0.0.1'
]

# Debug logging to verify settings are loaded
print(f"🔧 PRODUCTION SETTINGS LOADED - DEBUG={DEBUG}")

# Database - Use DATABASE_URL from environment
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS settings for production (adjust as needed)
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if os.environ.get('CORS_ALLOWED_ORIGINS') else []

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
