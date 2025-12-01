from pathlib import Path
from decouple import config
import os
from google.oauth2 import service_account
from google.auth import default as google_auth_default

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Sécurité
# -------------------------------
SECRET_KEY = config("SECRET_KEY", default="insecure-key")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "192.168.88.245",
    "freelance.stage",
    "backend",
    "localhost",
    "backend.freelance.svc.cluster.local"
]

FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")

# -------------------------------
# Applications installées
# -------------------------------
INSTALLED_APPS = [
    'django_prometheus',
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
    'storages',

    # Apps locales
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
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

PROMETHEUS_EXPORT_MIGRATIONS = False

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
    "http://localhost:5173",
    "http://192.168.88.27:5173",
    "http://192.168.88.245:80",
    "http://freelance.stage:80",
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()

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
if os.environ.get("CI") == "true":
    # Base super rapide pour les tests CI
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",  # DB en mémoire RAM → hyper rapide
        }
    }
else:
    # MySQL en local + production
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

# STATIC & MEDIA (LOCAL MODE)
# -------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------
# GOOGLE CLOUD STORAGE
# -------------------------------
if not DEBUG:

    GS_BUCKET_NAME = config("GS_BUCKET_NAME")
    GS_PROJECT_ID = config("GS_PROJECT_ID")

    # Chemin dans le conteneur (monté depuis un secret Kubernetes)
    GCS_KEY_PATH = "/secrets/key.json"

    # On charge la clé de service GCP
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GCS_KEY_PATH)

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": "media",  # dossier dans le bucket
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": "static",
            },
        },
    }

    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
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
