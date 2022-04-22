import pytest

from asgi_middleware_static_file.core import ASGIMiddlewareStaticFile
from .asgi_test_kit import ASGIApp, ASGITestClient, MOCK_APP_RESPONSE_SUCCESS


@pytest.mark.asyncio
async def test_all():
    app = ASGIApp()
    c = ASGITestClient(
        ASGIMiddlewareStaticFile(app=app, static_url="/static", static_root_paths=[])
    )

    r = await c.get("/")
    assert r.status_code == 200
    assert r.text == MOCK_APP_RESPONSE_SUCCESS

    r = await c.websocket("/")
    assert r.status_code == 200
