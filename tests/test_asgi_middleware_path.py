from pathlib import Path

import pytest

from asgi_middleware_static_file import ASGIMiddlewarePath

fsp_base = Path(__name__).resolve().parent / "example" / "example_static"
url_base = ASGIMiddlewarePath("/a/b/c/")


def test_join_path():
    assert url_base.join_path("d").path_as_str == "/a/b/c/d"
    assert url_base.join_path("d/e").path_as_str == "/a/b/c/d/e"


def test_startswith():
    assert url_base.startswith(ASGIMiddlewarePath("/a/b"))
    assert not url_base.startswith(ASGIMiddlewarePath("/a/b/c/e"))
    assert not url_base.startswith(ASGIMiddlewarePath("/x"))


@pytest.mark.asyncio
async def test_accessible():
    this_file = Path(__file__).resolve().as_posix()
    assert await ASGIMiddlewarePath(this_file).accessible()

    assert not await ASGIMiddlewarePath(fsp_base.joinpath("not_exists")).accessible()
    assert not await ASGIMiddlewarePath(fsp_base).accessible()  # is path
