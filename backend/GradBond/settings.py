import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# cloudinary imports
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = [
    "https://gradbond.up.railway.app",
]

SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ['127.0.0.1', 'gradbond.up.railway.app']
DEBUG = False


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'cloudinary',
    'import_export',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    
    # custom apps
    'authentication',
    'core',
    'apis',
    'corsheaders',

    # chatting
    'channels',
    'chat',
]

ASGI_APPLICATION = 'GradBond.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get("REDIS_URL")],
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

from corsheaders.defaults import default_headers
from pathlib import Path
from corsheaders.defaults import default_headers

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOW_HEADERS = list(default_headers) + [
    "content-type",
    "authorization",
    "x-csrftoken",
]

ROOT_URLCONF = 'GradBond.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'GradBond.wsgi.application'

# Use PostgreSQL, MySQL, or SQLite from .env
DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Use WhiteNoise for Static Files (DO NOT USE DROPBOX FOR STATICFILES)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# AutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


# JWT settings
JWT_SECRET_KEY = SECRET_KEY  # or use a separate secret
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600  # 1 hour
