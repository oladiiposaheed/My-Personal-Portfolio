"""
Django settings for portfolio project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environmental variable
load_dotenv()

# SECRET KEY
SECRET_KEY = config('SECRET_KEY')

# DEBUG = True

# ALLOWED_HOSTS = ['https://oladiiposaheed.site', 'oladiiposaheed.site', 'oladiiposaheed.site', 'my-personal-portfolio-production-f51f.up.railway.app', 'https://my-personal-portfolio-production-f51f.up.railway.app']
# CSRF_TRUSTED_ORIGINS = ['https://oladiiposaheed.site', 'https://my-personal-portfolio-production-f51f.up.railway.app']


DEBUG = False
ALLOWED_HOSTS = ['oladiiposaheed.site', 'www.oladiiposaheed.site', 'my-personal-portfolio-production-f51f.up.railway.app']

CSRF_TRUSTED_ORIGINS = ['https://oladiiposaheed.site', 'https://my-personal-portfolio-production-f51f.up.railway.app']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'projects',
    'certifications',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# FIXED: Use 'porfolio' to match your actual project name
ROOT_URLCONF = 'porfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.profile_data',
            ],
        },
    },
]

# FIXED: Use 'porfolio' to match your actual project name
WSGI_APPLICATION = 'porfolio.wsgi.application'

# Database configuration - Simple SQLite for local development
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER':'postgres',
        'PASSWORD':os.environ['DB_PASSWORD'],
        'HOST':'ballast.proxy.rlwy.net',
        'PORT':'58467',
        
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' #new
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# Static files configuration

# WhiteNoise storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' #new

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Create media directories if they don't exist
os.makedirs(MEDIA_ROOT / 'profile', exist_ok=True)
os.makedirs(MEDIA_ROOT / 'projects/main', exist_ok=True)
os.makedirs(MEDIA_ROOT / 'projects/gallery', exist_ok=True)
os.makedirs(MEDIA_ROOT / 'certifications', exist_ok=True)
os.makedirs(MEDIA_ROOT / 'resume', exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

