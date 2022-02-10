import os

from asgiref.wsgi import WsgiToAsgi

from asgi_middleware_static_file import ASGIMiddlewareStaticFile

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, "example_static")]


def wsgi_app(environ, start_response):
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    return ["Hello world!"]


app = ASGIMiddlewareStaticFile(
    WsgiToAsgi(wsgi_app), static_url="static", static_root_paths=STATIC_DIRS
)
