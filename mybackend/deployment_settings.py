import os
import dj_database_url
from .settings import *  # noqa

# =========================================================
# PROD / RENDER
# =========================================================
DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
CUSTOM_DOMAIN = os.getenv("CUSTOM_DOMAIN")

# Hosts
ALLOWED_HOSTS = []
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# Fallback (évite 400 "Bad Request" si host inattendu)
# Tu peux enlever si tu veux strict, mais utile pendant debug
ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

# =========================================================
# DRF (JSON only)
# =========================================================
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework_gis.pagination.GeoJsonPagination",
    "PAGE_SIZE": 1000,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# =========================================================
# DATABASE (POSTGIS) - OBLIGATOIRE
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required on Render.")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# =========================================================
# SECURITY (Render derrière proxy)
# =========================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ✅ Pour une API publique, on évite de forcer la redirection https côté Django
# (Render/Cloudflare gèrent déjà ça)
SECURE_SSL_REDIRECT = False

# =========================================================
# CORS (Frontend Vercel)
# =========================================================
CORS_ALLOW_ALL_ORIGINS = False

# ✅ Autorise TOUS les déploiements Vercel (preview + prod)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/.*\.vercel\.app$",
]

# Optionnel : ton domaine exact (si tu veux le garder)
# Mets ici TON URL Vercel actuelle (celle de l'erreur console)
CORS_ALLOWED_ORIGINS = [
    "https://senegal-frontend-f8q5-8hswi5gwj-ousus-projects-90bdaa8f.vercel.app",
]

# =========================================================
# CSRF (utile si tu fais des POST depuis navigateur avec cookies)
# Pour une API GET sans cookies : pas critique, mais on met propre.
# =========================================================
CSRF_TRUSTED_ORIGINS = [
    "https://senegal-frontend-f8q5-8hswi5gwj-ousus-projects-90bdaa8f.vercel.app",
    "https://senegal-frontend-f8q5.vercel.app",
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")
if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{CUSTOM_DOMAIN}")
