import os

from quart import Quart
from asgi_middleware_static_file import ASGIMiddlewareStaticFile

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'demo_static')]

app = Quart(__name__)


@app.route('/')
async def hello():
    return 'hello'


app = ASGIMiddlewareStaticFile(
    app, static_url='static', static_paths=STATIC_DIRS
)
