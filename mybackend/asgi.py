import os
from django.core.asgi import get_asgi_application

# Le plus fiable : laisser Render définir DJANGO_SETTINGS_MODULE
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "mybackend.settings")
)

application = get_asgi_application()
