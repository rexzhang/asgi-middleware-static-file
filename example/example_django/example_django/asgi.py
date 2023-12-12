"""
ASGI config for example_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from pathlib import Path

from django.conf import settings
from django.core.asgi import get_asgi_application

from asgi_middleware_static_file import ASGIMiddlewareStaticFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_django.settings")

# Django's `settings.STATIC_ROOT` is `example/example_django/staticfiles` in this example
# If your static files are distributed in several different directories, you can send a list to `static_root_paths`
outside_statice_path = Path(__file__).parent.parent.parent.joinpath("example_static")
print(outside_statice_path)

application = get_asgi_application()
application = ASGIMiddlewareStaticFile(
    application,
    static_url=settings.STATIC_URL,
    static_root_paths=[settings.STATIC_ROOT, outside_statice_path],
)
