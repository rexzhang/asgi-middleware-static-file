# ASGIMiddlewareStaticFile

![GitHub](https://img.shields.io/github/license/rexzhang/asgi-middleware-static-file)
[![](https://img.shields.io/pypi/v/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
[![](https://img.shields.io/pypi/pyversions/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
![Pytest Workflow Status](https://github.com/rexzhang/asgi-middleware-static-file/actions/workflows/check-pytest.yaml/badge.svg)
[![codecov](https://codecov.io/gh/rexzhang/asgi-middleware-static-file/branch/main/graph/badge.svg?token=083O4RHEZE)](https://codecov.io/gh/rexzhang/asgi-middleware-static-file)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ASGIMiddlewareStaticFile)

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

## Common

### Prepare
```shell
pip3 install -U ASGIMiddlewareStaticFile
git clone https://github.com/rexzhang/asgi-middleware-static-file.git
cd asgi-middleware-static-file/example
```

### Test with wget
```shell
(venv) ➜  example git:(main) ✗ wget http://127.0.0.1:8000/static/DEMO
--2022-02-10 16:02:07--  http://127.0.0.1:8000/static/DEMO
正在连接 127.0.0.1:8000... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：26 []
正在保存至: “DEMO”

DEMO                                   100%[===========================================================================>]      26  --.-KB/s  用时 0s      

2022-02-10 16:02:08 (529 KB/s) - 已保存 “DEMO” [26/26])
```

## [Pure ASGI](https://asgi.readthedocs.io/en/latest/introduction.html)
### Code 
[`example_pure_asgi.py`](example/example_pure_asgi.py)

### Start Server
```shell
(venv) ➜  example git:(main) ✗ uvicorn example_pure_asgi:app
INFO:     Started server process [7965]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:54529 - "GET /static/DEMO HTTP/1.1" 200 OK
```

## [Django](https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/)

### Code
[`/example_django/asgi.py`](example/example_django/example_django/asgi.py)

### Collect static file
```shell
cd example_django

(venv) ➜  example_django git:(main) ✗ python manage.py collectstatic

129 static files copied to '/Users/rex/p/asgi-middleware-static-file/example/example_django/staticfiles'.
```

### Start Server
```shell
(venv) ➜  example_django git:(main) ✗ uvicorn example_django.asgi:application
INFO:     Started server process [9107]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:61925 - "GET /static/DEMO.txt HTTP/1.1" 200 OK

```

## [Quart](https://pgjones.gitlab.io/quart/tutorials/quickstart.html) (Flask like)

### Code 
[`example_quart.py`](example/example_quart.py)

### Start Server
```shell
(venv) ➜  example git:(main) ✗ uvicorn example_quart:app    
INFO:     Started server process [7989]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56191 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:56212 - "GET /static/DEMO HTTP/1.1" 200 OK
```

# [WSGI app](https://www.python.org/dev/peps/pep-3333/)

# Code 
[`example_wsgi_app.py`](example/example_wsgi_app.py)

## Start Server
```shell
(venv) ➜  example git:(main) ✗ uvicorn example_wsgi_app:app
INFO:     Started server process [8020]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:63924 - "GET /static/DEMO HTTP/1.1" 200 OK
```

# History

## Version 0.3.2
- Maintenance release
- Drop Py35

## Version 0.3.1
- Compatible Py37-

## Version 0.3.0
- Check cross border access
- Add more type hints

## Version 0.2.1
- Fix bug

## Version 0.2.0
- Update for aiofiles
- Fix bug

## Version 0.1.0
- First release

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
