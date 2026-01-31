import os
from pathlib import Path

# =========================================================
# BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# GDAL / GEOS (Windows seulement)
# =========================================================
if os.name == "nt":
    os.environ.setdefault("OSGEO4W_ROOT", r"C:\OSGeo4W")
    os.environ.setdefault("GDAL_DATA", r"C:\OSGeo4W\share\gdal")
    os.environ.setdefault("PROJ_LIB", r"C:\OSGeo4W\share\proj")
    os.environ["PATH"] = r"C:\OSGeo4W\bin;" + os.environ.get("PATH", "")

    GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdal308.dll"
    GEOS_LIBRARY_PATH = r"C:\OSGeo4W\bin\geos_c.dll"

# =========================================================
# SECURITY / ENV
# =========================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # ex: sn221-django-1.onrender.com
ENV = os.getenv("ENV", "local").lower()  # local | production

IS_RENDER = bool(RENDER_EXTERNAL_HOSTNAME)
IS_PROD = (ENV == "production") or IS_RENDER

# =========================================================
# HOSTS
# =========================================================
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]
if IS_RENDER:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CUSTOM_DOMAIN = os.getenv("CUSTOM_DOMAIN")
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# =========================================================
# HTTPS / COOKIES
# - HTTPS seulement en prod/Render
# =========================================================
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

if IS_PROD:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"

# =========================================================
# APPS
# =========================================================
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

# =========================================================
# MIDDLEWARE (CorsMiddleware doit être avant CommonMiddleware)
# =========================================================
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

# Sur Render, DATABASE_URL doit exister
if IS_RENDER and not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required on Render.")

if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("POSTGRES_DB", "poweend"),
            "USER": os.getenv("POSTGRES_USER", "poweend"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "Poweend26"),
            "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# =========================================================
# STATIC FILES (WhiteNoise)
# =========================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
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
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================================
# CORS + CSRF
# =========================================================

# ✅ Simple et robuste :
# - en local : autoriser tout (évite les galères)
# - en prod : whitelist stricte
CORS_ALLOW_ALL_ORIGINS = not IS_PROD

# Si tu veux absolument contrôler par env en local, remplace la ligne ci-dessus par :
# CORS_ALLOW_ALL_ORIGINS = (not IS_PROD) and (os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").lower() == "true")

CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "False").lower() == "true"

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = [
        "https://frontend-dql2.vercel.app",
    ]
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https:\/\/frontend-dql2-.*\.vercel\.app$",
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
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_VARY_HEADER = True

# CSRF : en local (http) + en prod (https)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-dql2.vercel.app",
]
if IS_RENDER:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")
if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")

CSRF_TRUSTED_ORIGIN_REGEXES = [
    r"^https:\/\/frontend-dql2-.*\.vercel\.app$",
]

# =========================================================
# DRF
# =========================================================
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework_gis.pagination.GeoJsonPagination",
    "PAGE_SIZE": 1000,
}
