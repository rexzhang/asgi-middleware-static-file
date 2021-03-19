# ASGIMiddlewareStaticFile

[![](https://img.shields.io/pypi/v/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
[![](https://img.shields.io/pypi/pyversions/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
[![](https://img.shields.io/pypi/dm/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)

ASGI Middleware for serving static file.

# Why?

> ASGIMiddlewareStaticFile is a solution when we need to distribute the whole project with static files in Docker; when the deployment environment has very limited resources.

# Features

- Standard ASGI middleware implement
- Async file IO
- Support ETag(base on md5(file_size + last_modified) )

# Install

```shell
pip3 install -U ASGIMiddlewareStaticFile
```

# Usage

## [Pure ASGI](https://asgi.readthedocs.io/en/latest/introduction.html)

Code `demo_pure_asgi.py`

```python
import os
from asgi_middleware_static_file import ASGIMiddlewareStaticFile

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'demo_static')]


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
  app, static_url='static', static_root_paths=STATIC_DIRS
)
```

Run Server

```shell
(venv) ➜  asgi-middleware-static-file git:(master) ✗ uvicorn demo_pure_asgi:app
INFO:     Started server process [21061]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:54529 - "GET /static/DEMO HTTP/1.1" 200 OK
```

Run wget

```shell
(venv) ➜  asgi-middleware-static-file git:(master) ✗ wget http://127.0.0.1:8000/static/DEMO
--2021-01-11 19:54:24--  http://127.0.0.1:8000/static/DEMO
正在连接 127.0.0.1:8000... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：26 []
正在保存至: “DEMO.6”

DEMO.6                        100%[==============================================>]      26  --.-KB/s  用时 0s

2021-01-11 19:54:24 (540 KB/s) - 已保存 “DEMO.6” [26/26])
```

## [Django](https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/)

Update file [example/django_example/django_example/asgi.py](https://github.com/rexzhang/asgi-middleware-static-file/blob/master/example/django_example/django_example/asgi.py)

```python
"""
ASGI config for django_example project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from asgi_middleware_static_file import ASGIMiddlewareStaticFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_example.settings')

application = get_asgi_application()
application = ASGIMiddlewareStaticFile(
  application, static_url=settings.STATIC_URL,
  static_root_paths=[settings.STATIC_ROOT]
)
```

Do't forget execute

```shell
python manage.py collectstatic
133 static files copied to '/Users/rex/p/asgi-middleware-static-file/example/django_example/staticfiles'.
```

Run server

```shell
uvicorn django_example.asgi:application
INFO:     Started server process [93869]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:61925 - "GET /static/DEMO.txt HTTP/1.1" 200 OK

```

## [Quart](https://pgjones.gitlab.io/quart/tutorials/quickstart.html) (Flask like)

### Code `demo_quart.py`

```python
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
  app, static_url='static', static_root_paths=STATIC_DIRS
)
```

### Run Server

```shell
(venv) ➜  asgi-middleware-static-file git:(master) ✗ uvicorn demo_quart:app        
INFO:     Started server process [22289]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56191 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:56212 - "GET /static/DEMO HTTP/1.1" 200 OK
```

### Run wget

```shell
(venv) ➜  asgi-middleware-static-file git:(master) ✗ wget http://127.0.0.1:8000/static/DEMO
--2021-01-11 20:17:46--  http://127.0.0.1:8000/static/DEMO
正在连接 127.0.0.1:8000... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：26 []
正在保存至: “DEMO.7”

DEMO.7                        100%[==============================================>]      26  --.-KB/s  用时 0s

2021-01-11 20:17:46 (1.46 MB/s) - 已保存 “DEMO.7” [26/26])
```

# Alternative

- ASGI Middleware
    - django.contrib.staticfiles.handlers.ASGIStaticFilesHandler

- WSGI Middleware
    - <https://github.com/kobinpy/wsgi-static-middleware>
    - <https://pypi.org/project/whitenoise/>

- View
    - starlette.staticfiles.StaticFiles

# TODO

- zero copy
- file extension filter,
- Cache Control
