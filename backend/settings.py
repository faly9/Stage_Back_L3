from pathlib import Path
from decouple import config
import os 

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Sécurité
# -------------------------------
SECRET_KEY = config("SECRET_KEY", default="insecure-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = ["*"]
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")

# -------------------------------
# Applications installées
# -------------------------------
INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',

    # apps locales
    'authentification',
    'entreprise',
    'mission',
    'freelance',
    'candidature',
]

SITE_ID = 1

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
] 

# -------------------------------
# DRF & Auth
# -------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# -------------------------------
# CORS pour React
# -------------------------------
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://frontend",
    "http://frontend:80",
    # ✅ inclure le port NodePort si utilisé
]

CORS_ALLOWED_ORIGINS = [
    "http://frontend",
    "http://frontend:80",
]

# -------------------------------
# URLs et Templates
# -------------------------------
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = "backend.asgi.application"

# -------------------------------
# Base de données MySQL
# -------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST", default="localhost"),
        'PORT': config("DB_PORT", default="3306"),
    }
}

AUTH_USER_MODEL = 'authentification.User'

# -------------------------------
# Validation des mots de passe
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# Email
# -------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -------------------------------
# Internationalisation
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Indian/Antananarivo"
USE_I18N = True
USE_TZ = True

# -------------------------------
# Fichiers statiques et médias
# -------------------------------
STATIC_URL = '/static/'
MEDIA_URL = config("MEDIA_URL", default="http://192.168.88.245:30000/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------------
# Channels / Redis
# -------------------------------
REDIS_HOST = config("REDIS_HOST", default="127.0.0.1")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# -------------------------------
# Clé primaire par défaut
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
