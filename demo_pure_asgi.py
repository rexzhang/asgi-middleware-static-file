import os
from asgi_middleware_static_file import ASGIMiddlewareStaticFile

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]


async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })


app = ASGIMiddlewareStaticFile(
    app, static_url='static', static_paths=STATIC_DIRS
)
