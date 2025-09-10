from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

    # SECURITY WARNING: keep the secret key used in production secret!
    # 'decouple' will look for a SECRET_KEY environment variable.
SECRET_KEY = config('SECRET_KEY')

    # SECURITY WARNING: don't run with debug turned on in production!
    # Default to False. Set DEBUG=True as an environment variable for local dev.
DEBUG = config('DEBUG', default=False, cast=bool)

    # List of allowed hosts. Render will automatically handle this, 
    # but for other platforms you might need to add your domain here.
ALLOWED_HOSTS = []

    # Application definition
INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        # Add WhiteNoise for serving static files
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.staticfiles',
        # My Apps
        'core',
        'transactions',
        'transactions.templatetags', # Add this for our custom filter
    ]

MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        # WhiteNoise middleware should be placed right after SecurityMiddleware
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'finsight_project.urls'

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

WSGI_APPLICATION = 'finsight_project.wsgi.application'

    # Database
    # This will use the DATABASE_URL from Render's environment, 
    # or fallback to our local SQLite database if it's not set.
DATABASES = {
        'default': dj_database_url.config(
            default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
        )
    }

    # Password validation
AUTH_PASSWORD_VALIDATORS = [
        # ... (validators are unchanged) ...
    ]

    # Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

    # Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
    # The directory where Django will collect all static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # The storage engine that compresses files and handles caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
    

