import os
from pathlib import Path

# =========================================================
# BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY / ENV
# =========================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")

# DEBUG: False en prod
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Render fournit souvent ce hostname automatiquement
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# ALLOWED_HOSTS
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# (Optionnel) si tu connais le hostname Render exact :
# ALLOWED_HOSTS.append("sn221-django-1.onrender.com")

# Si tu es derrière un proxy (Render), utile pour https
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Optionnel (souvent OK sur Render, mais active seulement si tu veux forcer https)
    # SECURE_SSL_REDIRECT = True

# =========================================================
# APPS
# =========================================================
INSTALLED_APPS = [
    # CORS doit être installé
    "corsheaders",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # GIS
    "django.contrib.gis",

    # DRF
    "rest_framework",
    "rest_framework_gis",

    # Ton app
    "maps",
]

# =========================================================
# MIDDLEWARE (ORDRE CRITIQUE)
# =========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # CorsMiddleware doit être le plus haut possible, AVANT CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    # WhiteNoise pour les fichiers statiques (utile en prod)
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================================================
# URLS / WSGI / ASGI
# =========================================================
ROOT_URLCONF = "mybackend.urls"
WSGI_APPLICATION = "mybackend.wsgi.application"
ASGI_APPLICATION = "mybackend.asgi.application"

# =========================================================
# TEMPLATES
# =========================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# =========================================================
# DATABASE (PostGIS)
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    # Force PostGIS engine (utile si Render fournit postgres classique)
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
else:
    # Fallback local (évite les mots de passe codés en dur)
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("POSTGRES_DB", "poweend"),
            "USER": os.getenv("POSTGRES_USER", "poweend"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# =========================================================
# STATIC FILES (WhiteNoise)
# =========================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# =========================================================
# I18N
# =========================================================
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================================
# CORS + CSRF (Vercel + local) - PROPRE
# =========================================================

# IMPORTANT :
# - En prod, laisse False et utilise CORS_ALLOWED_ORIGINS
# - En debug, tu peux mettre True via variable d'env si tu veux tester vite
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").lower() == "true"

CORS_ALLOWED_ORIGINS = [
    # Local dev (Vite)
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # Vercel production
    "https://frontend-dql2.vercel.app",
]

# Si tu utilises les preview deployments Vercel, décommente ceci :
# (ça autorise https://frontend-xxxxx.vercel.app)
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https:\/\/frontend-.*\.vercel\.app$",
# ]

# Si tu utilises cookies/auth par session, mets True (sinon laisse False)
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "False").lower() == "true"

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Pour les POST/PUT avec CSRF (souvent inutile pour API token-based)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-dql2.vercel.app",
]

# =========================================================
# DRF (OPTIONNEL, mais pratique)
# =========================================================
REST_FRAMEWORK = {
    # Tu peux activer l’auth plus tard
    # "DEFAULT_AUTHENTICATION_CLASSES": [],
    # "DEFAULT_PERMISSION_CLASSES": [],
}

# =========================================================
# GDAL / GEOS (Windows seulement - dev)
# =========================================================
if os.name == "nt":
    os.environ.setdefault("OSGEO4W_ROOT", r"C:\OSGeo4W")
    os.environ.setdefault("GDAL_DATA", r"C:\OSGeo4W\share\gdal")
    os.environ.setdefault("PROJ_LIB", r"C:\OSGeo4W\share\proj")
    os.environ["PATH"] = r"C:\OSGeo4W\bin;" + os.environ.get("PATH", "")

    # Adapte selon ta version installée
    GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdal308.dll"
    GEOS_LIBRARY_PATH = r"C:\OSGeo4W\bin\geos_c.dll"
