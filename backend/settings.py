from pathlib import Path
from decouple import config
import os
from google.oauth2 import service_account
from google.auth import default as google_auth_default # Pour l'authentification via Workload Identity

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
    # Ajoutez ici les FQDN publics si vous en avez
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
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CORS_ALLOW_CREDENTIALS = True

# Utilisation de config() pour les origines de CORS
CORS_TRUSTED_ORIGINS = [
    "http://frontend",
    "http://frontend:80",
    "http://localhost:5173",
    "http://192.168.88.27:5173",
    "http://192.168.88.245:80",
    "http://freelance.stage:80",
]
# Ajouter les origines définies par l'environnement si nécessaire
CORS_TRUSTED_ORIGINS.extend(config("CORS_TRUSTED_ORIGINS", default="", cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]))

CORS_ALLOWED_ORIGINS = CORS_TRUSTED_ORIGINS.copy()

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
        'PORT': config("DB_PORT", default="3306", cast=int),
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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Utilisé uniquement en mode développement (DEBUG=True)

# Configuration de Google Cloud Storage (GCS)
GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="freelance-media")
GS_PROJECT_ID = config("GS_PROJECT_ID", default=None)
GS_DEFAULT_ACL = None 
GS_LOCATION = 'auto' # Optionnel, pour spécifier la région
GS_CREDENTIALS = None

# Tente de charger les identifiants depuis un fichier JSON (pour dev/tests locaux ou environnements spécifiques)
if os.path.exists(os.path.join(BASE_DIR, "gcs-key.json")):
    try:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.path.join(BASE_DIR, "gcs-key.json")
        )
    except Exception as e:
        # En cas d'erreur de chargement (fichier corrompu, etc.)
        print(f"Avertissement: Impossible de charger 'gcs-key.json'. Utilisation de l'authentification par défaut. Erreur: {e}")
        pass


if not DEBUG:
    # --- Mode Production (GCS) ---
    
    # Si GS_CREDENTIALS n'est pas chargé (et que nous sommes sur GCP/GKE),
    # il est préférable de laisser google-cloud-storage utiliser Workload Identity 
    # ou les identifiants par défaut du service.
    if GS_CREDENTIALS is None:
        try:
             # Utilise Workload Identity ou les identifiants d'environnement GKE/Cloud Run
            GS_CREDENTIALS, _ = google_auth_default()
            print("INFO: Utilisation des identifiants Google Cloud par défaut (Workload Identity, etc.).")
        except Exception as e:
            print(f"ATTENTION: Impossible d'obtenir les identifiants par défaut pour GCS. Assurez-vous que Workload Identity est configuré. Erreur: {e}")
            pass

    # Utilisation de la nouvelle syntaxe `STORAGES` (Django 4.2+)
    STORAGES = {
        # Fichiers média (images)
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": 'media', # Optionnel: stocke tous les uploads dans un sous-dossier 'media/' du bucket
            }
        },
        # Fichiers statiques
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
                "credentials": GS_CREDENTIALS,
                "location": 'static', # Optionnel: stocke tous les statics dans un sous-dossier 'static/' du bucket
            }
        }
    }
    
    # URL de base pour les fichiers médias (pour que les modèles y fassent référence)
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/" 
    
    # URL de base pour les fichiers statiques (pour collectstatic)
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

else:
    # --- Mode Développement Local (DEBUG=True) ---
    MEDIA_URL = '/media/'
    # Utilisation de la nouvelle syntaxe `STORAGES` (Django 4.2+)
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        }
    }


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