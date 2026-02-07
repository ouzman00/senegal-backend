import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# Core
# ---------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ENV = os.getenv("ENV", "local").lower()
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
CUSTOM_DOMAIN = os.getenv("CUSTOM_DOMAIN")

IS_RENDER = bool(RENDER_EXTERNAL_HOSTNAME)
IS_PROD = (ENV == "production") or IS_RENDER

# ---------------------------------------------------------
# GeoDjango libs
#   IMPORTANT: never set Windows paths on Linux/Render
# ---------------------------------------------------------
if os.name == "nt":
    # If you use OSGeo4W (recommended)
    OSGEO4W_ROOT = os.getenv("OSGEO4W_ROOT", r"C:\OSGeo4W")
    os.environ.setdefault("OSGEO4W_ROOT", OSGEO4W_ROOT)
    os.environ.setdefault("GDAL_DATA", rf"{OSGEO4W_ROOT}\share\gdal")
    os.environ.setdefault("PROJ_LIB", rf"{OSGEO4W_ROOT}\share\proj")
    os.environ["PATH"] = rf"{OSGEO4W_ROOT}\bin;" + os.environ.get("PATH", "")

    # Prefer stable dll names
    GDAL_LIBRARY_PATH = rf"{OSGEO4W_ROOT}\bin\gdal.dll"
    GEOS_LIBRARY_PATH = rf"{OSGEO4W_ROOT}\bin\geos_c.dll"

# On Linux (Render), do NOT set GDAL_LIBRARY_PATH/GEOS_LIBRARY_PATH.
# System packages provide libgdal/libgeos and Django finds them.

# ---------------------------------------------------------
# Hosts
# ---------------------------------------------------------
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]
if IS_RENDER:
    # Render hostname + wildcard for safety
    ALLOWED_HOSTS += [RENDER_EXTERNAL_HOSTNAME, ".onrender.com"]
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# ---------------------------------------------------------
# Apps
# ---------------------------------------------------------
INSTALLED_APPS = [
    "corsheaders",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.gis",

    "rest_framework",
    "rest_framework_gis",

    "maps",
]

# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mybackend.urls"
WSGI_APPLICATION = "mybackend.wsgi.application"
ASGI_APPLICATION = "mybackend.asgi.application"

# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Database (PostGIS)
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # Local (set these in .env locally; DO NOT hardcode passwords)
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("POSTGRES_DB", "geomap"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Force PostGIS engine even when DATABASE_URL is used
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

# ---------------------------------------------------------
# I18N / TZ
# ---------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------
# Security (Render behind proxy)
# ---------------------------------------------------------
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

if IS_PROD:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Render/Cloudflare handle HTTPS

# ---------------------------------------------------------
# CORS / CSRF
# ---------------------------------------------------------
CORS_ALLOW_CREDENTIALS = False

if IS_PROD:
    CORS_ALLOW_ALL_ORIGINS = False

    # Allow all Vercel deployments (preview + prod)
    CORS_ALLOWED_ORIGIN_REGEXES = [r"^https:\/\/.*\.vercel\.app$"]

    # Optional stable prod domain
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "").strip()
    CORS_ALLOWED_ORIGINS = [FRONTEND_ORIGIN] if FRONTEND_ORIGIN else []

    CSRF_TRUSTED_ORIGINS = []
    if FRONTEND_ORIGIN:
        CSRF_TRUSTED_ORIGINS.append(FRONTEND_ORIGIN)
    if RENDER_EXTERNAL_HOSTNAME:
        CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")
    if CUSTOM_DOMAIN:
        CSRF_TRUSTED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")
else:
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

# ---------------------------------------------------------
# DRF
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework_gis.pagination.GeoJsonPagination",
    "PAGE_SIZE": 1000,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}
