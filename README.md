# ASGIMiddlewareStaticFile

![GitHub](https://img.shields.io/github/license/rexzhang/asgi-middleware-static-file)
[![](https://img.shields.io/pypi/v/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
[![](https://img.shields.io/pypi/pyversions/ASGIMiddlewareStaticFile.svg)](https://pypi.org/project/ASGIMiddlewareStaticFile/)
![Pytest Workflow Status](https://github.com/rexzhang/asgi-middleware-static-file/actions/workflows/check-pytest.yaml/badge.svg)
[![codecov](https://codecov.io/gh/rexzhang/asgi-middleware-static-file/branch/main/graph/badge.svg?token=083O4RHEZE)](https://codecov.io/gh/rexzhang/asgi-middleware-static-file)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ASGIMiddlewareStaticFile)

ASGI Middleware for serving static file.

## Why?

> ASGIMiddlewareStaticFile is a solution when we need to distribute the whole project with static files in Docker; or
> when the deployment environment has very limited resources; or Internal network(Unable to reach CDN).

## Features

- Standard ASGI middleware implement
- Async file IO
- Support ETag, base on md5(file_size + last_modified)

## Install

```shell
pip3 install -U ASGIMiddlewareStaticFile
```

## Usage

### Common

#### Prepare

```shell
pip3 install -U ASGIMiddlewareStaticFile
git clone https://github.com/rexzhang/asgi-middleware-static-file.git
cd asgi-middleware-static-file/example
```

#### Test with wget

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

### [Pure ASGI](https://asgi.readthedocs.io/en/latest/introduction.html)

#### Code

[`example_pure_asgi.py`](https://github.com/rexzhang/asgi-middleware-static-file/blob/main/example/example_pure_asgi.py)

#### Start Server

```shell
(venv) ➜  example git:(main) ✗ uvicorn example_pure_asgi:app
```

### [Django](https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/) 3.0+

#### Code

[`/example_django/asgi.py`](https://github.com/rexzhang/asgi-middleware-static-file/blob/main/example/example_django/example_django/asgi.py)

#### Collect static file

```shell
(venv) ➜  example git:(main) cd example_django
(venv) ➜  example_django git:(main) ✗ python manage.py collectstatic

129 static files copied to '/Users/rex/p/asgi-middleware-static-file/example/example_django/staticfiles'.
```

#### Start Server

```shell
(venv) ➜  example_django git:(main) ✗ uvicorn example_django.asgi:application
```

### [Quart](https://pgjones.gitlab.io/quart/tutorials/quickstart.html) (Flask like)

#### Code

[`example_quart.py`](https://github.com/rexzhang/asgi-middleware-static-file/blob/main/example/example_quart.py)

#### Start Server

```shell
(venv) ➜  example git:(main) ✗ uvicorn example_quart:app
```

### [WSGI app](https://www.python.org/dev/peps/pep-3333/) eg: Flask, Django on WSGI mode

#### Code

[`example_wsgi_app.py`](https://github.com/rexzhang/asgi-middleware-static-file/blob/main/example/example_wsgi_app.py)

#### Start Server

```
(venv) ➜  example git:(main) ✗ uvicorn example_wsgi_app:app
```

## FAQ

### My static files are distributed in several different directories

You can send a list to `static_root_paths`; example:

```python
static_root_paths = [ "/path/a", "path/b" ]
application = ASGIMiddlewareStaticFile(
    application,
    static_url=settings.STATIC_URL,
    static_root_paths=static_root_paths,
)
```

## History

### 0.6.2 - 20251112

- Maintenance update

### 0.6.1 - 20231219

- Maintenance update
- Change depend policy

### 0.6.0 - 20230210

- Update aiofiles to 23.1.0
- Use more async API

### 0.5.0 - 20220909

- Use more aiofiles api
- Dropped Python 3.6 support. If you require it, use version 0.4.0
- Update package for pep517/pep621

### v0.4.0 - 20220422

- Rewrite some code
- Fix bug #3(Cannot serve files from root (static_url="/" becomes "//"))

### v0.3.2

- Maintenance release
- Drop Py35

### v0.3.1

- Compatible Py37-

### v0.3.0

- Check cross border access
- Add more type hints

### v0.2.1

- Fix bug

### v0.2.0

- Update for aiofiles
- Fix bug

### v0.1.0

- First release

## Alternative

- ASGI Middleware
  - django.contrib.staticfiles.handlers.ASGIStaticFilesHandler
- WSGI Middleware
  - <https://github.com/kobinpy/wsgi-static-middleware>
  - <https://pypi.org/project/whitenoise/>

- View
  - starlette.staticfiles.StaticFiles

## TODO

- zero copy
- file extension filter,
- Cache Control
