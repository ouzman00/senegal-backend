import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY / ENV
# =========================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")

# DEBUG doit être False en prod (Render)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Render fournit automatiquement ce hostname
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# ALLOWED_HOSTS
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# (optionnel) sécurité en prod si tu veux forcer https derrière proxy Render
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================================================
# APPS
# =========================================================
INSTALLED_APPS = [
    "corsheaders",  # CORS
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
# MIDDLEWARE (ORDRE CRITIQUE)
# =========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # ⬅️ MUST be high, before CommonMiddleware
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

    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": os.getenv("POSTGRES_DB", "poweend"),
            "USER": os.getenv("POSTGRES_USER", "poweend"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "Poweend26"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# =========================================================
# STATIC FILES
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
# CORS + CSRF (Vercel + local)
# =========================================================
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    # Local dev
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Vercel
    "https://frontend-beta-rust-54.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-beta-rust-54.vercel.app",
]

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
