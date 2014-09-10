"""
Django settings for news project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#mmm(c*ezo)q(!z3@7xdcrgv88960a5ryvz2+8n1i235tr2r4d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.eggs.Loader',
]

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.sites',
    'south',
    'core',
    'price',
    'scheduler_manager'
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'scheduler_manager.urls'

WSGI_APPLICATION = 'news.core_wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'GMT+3:30'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),  # Assuming BASE_DIR is where your manage.py file is
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    # 'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
DEFAULT_LOGIN_URL = '/'
DEFAULT_LOGOUT_URL = '/'

# Mail Setting
DEFAULT_FROM_EMAIL = 'noreply@onlinecademy.com'
EMAIL_HOST = 'smtp.onlinecademy.com'
EMAIL_HOST_PASSWORD = 'sorooshMAHDI123'
EMAIL_HOST_USER = 'admin'
EMAIL_SUBJECT_PREFIX = 'Khabar-chin : '

SERVER_BASE_ADDRESS = 'http://localhost:8003'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'queries_above_300ms': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.duration > 0.0  # output slow queries only
        },
    },
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'price_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "price_logs.txt"),
            'maxBytes': 50000000,
            'backupCount': 2,
            'formatter': 'standard',
            # 'filters': ['queries_above_300ms'],
        },
        'rss_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "rss_logs.txt"),
            'maxBytes': 50000000,
            'backupCount': 2,
            'formatter': 'standard',
            # 'filters': ['queries_above_300ms'],
        },
        'crawler_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "crawler_logs.txt"),
            'maxBytes': 50000000,
            'backupCount': 2,
            'formatter': 'standard',
            # 'filters': ['queries_above_300ms'],
        },
        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "error.txt"),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'price_scheduler': {
            'handlers': ['price_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rss_scheduler': {
            'handlers': ['rss_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'crawler_scheduler': {
            'handlers': ['crawler_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'error': {
            'handlers': ['error_logfile', 'console'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
