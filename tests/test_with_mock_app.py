from pathlib import Path

import pytest

from asgi_middleware_static_file.core import ASGIMiddlewareStaticFile

from .asgi_test_kit import MOCK_APP_RESPONSE_SUCCESS, ASGIApp, ASGITestClient

static_root_path = Path(__file__).parent.joinpath("static")

TEXT_FILE_CONTENT = "this is a text file"


def get_client(static_url="/static"):
    app = ASGIApp()
    c = ASGITestClient(
        ASGIMiddlewareStaticFile(
            app=app, static_url=static_url, static_root_paths=[static_root_path]
        )
    )
    return c


@pytest.mark.asyncio
async def test_scope_type():
    c = get_client()

    # websocket
    r = await c.websocket("/")
    assert r.status_code == 200

    # http
    r = await c.get("/")
    assert r.status_code == 200
    assert r.text == MOCK_APP_RESPONSE_SUCCESS


@pytest.mark.asyncio
async def test_method_head():
    c = get_client()

    r = await c.head("/")
    assert r.status_code == 200
    assert r.text == MOCK_APP_RESPONSE_SUCCESS

    r = await c.head("/static/text-file.txt")
    assert r.status_code == 200
    assert r.text == ""

    r = await c.head("/static/does-not-exist.txt")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_method_get():
    c = get_client()

    r = await c.get("/")
    assert r.status_code == 200
    assert r.text == MOCK_APP_RESPONSE_SUCCESS

    r = await c.get("/static/text-file.txt")
    assert r.status_code == 200
    assert r.text == TEXT_FILE_CONTENT

    r = await c.get("/static/does-not-exist.txt")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_method_not_allowed():
    c = get_client()
    r = await c.options("/static/", headers={})
    assert r.status_code == 405


@pytest.mark.asyncio
async def test_cross_border_access():
    c = get_client()
    r = await c.get("/static/../aaa", headers={})
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_special_static_url():
    c = get_client(static_url="/")

    r = await c.get("/")
    assert r.status_code == 404

    r = await c.get("/text-file.txt")
    assert r.status_code == 200
    assert r.text == TEXT_FILE_CONTENT
