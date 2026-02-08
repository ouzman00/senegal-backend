import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# Core
# =========================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ENV = os.getenv("ENV", "local").lower()
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
CUSTOM_DOMAIN = os.getenv("CUSTOM_DOMAIN")

IS_RENDER = bool(RENDER_EXTERNAL_HOSTNAME)
IS_PROD = (ENV == "production") or IS_RENDER

# =========================================================
# GeoDjango (Windows only)
# =========================================================
if os.name == "nt":
    OSGEO4W_ROOT = os.getenv("OSGEO4W_ROOT", r"C:\OSGeo4W")

    os.environ.setdefault("OSGEO4W_ROOT", OSGEO4W_ROOT)
    os.environ.setdefault("GDAL_DATA", rf"{OSGEO4W_ROOT}\share\gdal")
    os.environ.setdefault("PROJ_LIB", rf"{OSGEO4W_ROOT}\share\proj")
    os.environ["PATH"] = rf"{OSGEO4W_ROOT}\bin;" + os.environ.get("PATH", "")

    _gdal_candidates = [
        "gdal313.dll", "gdal312.dll", "gdal311.dll", "gdal310.dll",
        "gdal309.dll", "gdal308.dll", "gdal307.dll", "gdal306.dll",
        "gdal305.dll", "gdal304.dll", "gdal303.dll", "gdal302.dll",
        "gdal301.dll",
    ]

    GDAL_LIBRARY_PATH = None
    for dll in _gdal_candidates:
        candidate = rf"{OSGEO4W_ROOT}\bin\{dll}"
        if os.path.exists(candidate):
            GDAL_LIBRARY_PATH = candidate
            break

    GEOS_LIBRARY_PATH = rf"{OSGEO4W_ROOT}\bin\geos_c.dll"

    if not GDAL_LIBRARY_PATH:
        raise RuntimeError(
            "GDAL introuvable. Vérifie OSGeo4W.\n"
            f"- OSGEO4W_ROOT={OSGEO4W_ROOT}\n"
            "Attendu: C:\\OSGeo4W\\bin\\gdal3xx.dll\n"
            "Astuce: PowerShell -> dir C:\\OSGeo4W\\bin\\gdal*.dll"
        )

    if not os.path.exists(GEOS_LIBRARY_PATH):
        raise RuntimeError(
            "GEOS introuvable. Vérifie OSGeo4W.\n"
            f"Attendu: {GEOS_LIBRARY_PATH}"
        )

# =========================================================
# Hosts
# =========================================================
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

if IS_RENDER and RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS += [RENDER_EXTERNAL_HOSTNAME, ".onrender.com"]

if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# =========================================================
# Apps
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
# Middleware
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
# URLs / WSGI / ASGI
# =========================================================
ROOT_URLCONF = "mybackend.urls"
WSGI_APPLICATION = "mybackend.wsgi.application"
ASGI_APPLICATION = "mybackend.asgi.application"

# =========================================================
# Templates
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
# Database (PostGIS)
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
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

DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# =========================================================
# Static files
# =========================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

# =========================================================
# I18N / TZ
# =========================================================
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================================
# Auth validators (standard)
# =========================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================================================
# Security (Render behind proxy)
# =========================================================
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

if IS_PROD:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False  # Render/Cloudflare

# =========================================================
# CORS / CSRF
# =========================================================
CORS_ALLOW_CREDENTIALS = False

if IS_PROD:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGIN_REGEXES = [r"^https:\/\/.*\.vercel\.app$"]

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

# =========================================================
# DRF
# =========================================================
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework_gis.pagination.GeoJsonPagination",
    "PAGE_SIZE": 1000,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# =========================================================
# Logging minimal (utile en prod)
# =========================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
