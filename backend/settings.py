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
    "backend.freelance.svc.cluster.local",
]

FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")

# -------------------------------
# Applications
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

    # Local apps
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

# -------------------------------
# DRF
# -------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# -------------------------------
# CORS / CSRF
# -------------------------------
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CORS_ALLOW_CREDENTIALS = True

# --- Oranges CORS principales ---
CORS_TRUSTED_ORIGINS = [
    "http://frontend",
    "http://frontend:80",
    "http://localhost:5173",
    "http://192.168.88.27:5173",
    "http://192.168.88.245",
    "http://freelance.stage",
]

# Ajout dynamique via variables d’environnement
CORS_TRUSTED_ORIGINS.extend(
    config("CORS_TRUSTED_ORIGINS",
           default="",
           cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])
)

CORS_ALLOWED_ORIGINS = CORS_TRUSTED_ORIGINS.copy()

# CSRF conforme Django 4+
CSRF_TRUSTED_ORIGINS = [o.replace("http://", "http://").replace("https://", "https://") for o in CORS_TRUSTED_ORIGINS]

# -------------------------------
# Templates
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
# Database
# -------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST", default="localhost"),
        'PORT': config("DB_PORT", default=3306, cast=int),
    }
}

AUTH_USER_MODEL = 'authentification.User'

# -------------------------------
# Password validators
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# Emails
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
# Static & Media
# -------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -------------------------------
# Google Cloud Storage (Prod)
# -------------------------------
GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="freelance-media")
GS_PROJECT_ID = config("GS_PROJECT_ID", default="soutenance-479118")
GS_DEFAULT_ACL = None
GS_CREDENTIALS = None

# Charge gcs-key.json si présent
if os.path.exists(os.path.join(BASE_DIR, "gcs-key.json")):
    try:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.path.join(BASE_DIR, "gcs-key.json")
        )
    except Exception as e:
        print("Erreur chargement gcs-key.json:", e)

if not DEBUG:
    # Workload Identity
    if GS_CREDENTIALS is None:
        try:
            GS_CREDENTIALS, _ = google_auth_default()
        except:
            pass

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": "media",
            }
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": "static",
            }
        }
    }

    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

# -------------------------------
# Redis / Channels
# -------------------------------
REDIS_HOST = config("REDIS_HOST", default="127.0.0.1")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(REDIS_HOST, REDIS_PORT)]},
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
