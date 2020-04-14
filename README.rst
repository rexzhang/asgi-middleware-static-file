========================
ASGIMiddlewareStaticFile
========================

ASGI Middleware for serving Static File.


Usage
=====

Pure ASGI
---------

.. code-block:: python

    import os
    from wsgiref.simple_server import make_server
    from asgi_middleware_static_file import ASGIMiddlewareStaticFile

    BASE_DIR = os.path.dirname(__name__)
    STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]


    def app(env, start_response):
        start_response('200 OK', [('Conte-type', 'text/plain; charset=utf-8')])
        return [b'Hello World']

    app = ASGIMiddlewareStaticFile(app, static_url='static', static_paths=STATIC_DIRS)

    if __name__ == '__main__':
        httpd = make_server('', 8000, app)
        httpd.serve_forever()

Django
------

Update ``asgi.py``

.. code-block:: python


    import os

    from django.conf import settings
    from django.core.asgi import get_asgi_application
    from asgi_middleware_static_file import ASGIMiddlewareStaticFile

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_project.settings')
    application = get_asgi_application()
    application = ASGIMiddlewareStaticFile(
        application, static_url=settings.STATIC_URL, static_paths=[settings.STATIC_ROOT]
    )


Do't forget execute ``python manage.py collectstatic``

try it

.. code-block:: console

    daphne dj_project.asgi:application -b 0.0.0.0


Alternative
===========

- django.contrib.staticfiles.handlers.ASGIStaticFilesHandler
- https://github.com/kobinpy/wsgi-static-middleware only work with WSGI
