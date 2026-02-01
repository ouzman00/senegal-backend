import os
import dj_database_url
from .settings import *  # importe tout de settings.py

# =========================================================
# PROD / RENDER
# =========================================================
DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    # fallback au cas où
    ALLOWED_HOSTS = ["*"]

# (optionnel) si tu as un domaine custom
CUSTOM_DOMAIN = os.getenv("CUSTOM_DOMAIN")
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# =========================================================
# DATABASE (POSTGIS) - OBLIGATOIRE
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required on Render.")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}
# ✅ CRUCIAL POUR GEODJANGO
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# =========================================================
# SECURITY (HTTPS derrière proxy Render)
# =========================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# (optionnel) si tu veux forcer https
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() == "true"

# =========================================================
# STATIC (WhiteNoise)
# =========================================================
# Tu as déjà WhiteNoise dans settings.py, rien de spécial ici.

# =========================================================
# CORS / CSRF (si tu as un frontend Vercel)
# =========================================================
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://frontend-dql2.vercel.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/frontend-dql2-.*\.vercel\.app$",
]

CSRF_TRUSTED_ORIGINS = [
    "https://frontend-dql2.vercel.app",
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")

SECURE_SSL_REDIRECT = False
