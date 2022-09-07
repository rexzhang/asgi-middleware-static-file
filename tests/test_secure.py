import pathlib

import pytest

from asgi_middleware_static_file import ASGIMiddlewareStaticFile

BASE_PATH = pathlib.Path(__name__).resolve().parent / "example" / "example_static"


@pytest.mark.asyncio
async def test_cross_border_access():
    print(BASE_PATH)
    mw = ASGIMiddlewareStaticFile(None, "static", [BASE_PATH])

    assert isinstance(await mw.locate_the_file("DEMO"), str)
    assert await mw.locate_the_file("not_found") is None

    with pytest.raises(ValueError):
        await mw.locate_the_file("../pyproject.toml")
