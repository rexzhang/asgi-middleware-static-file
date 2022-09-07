from pathlib import Path

import pytest

from asgi_middleware_static_file import ASGIMiddlewarePath

path = ASGIMiddlewarePath("/a/b/c/")


def test_join_path():
    assert path.join_path("d").path_as_str == "/a/b/c/d"
    assert path.join_path("d/e").path_as_str == "/a/b/c/d/e"


def test_startswith():
    assert path.startswith(ASGIMiddlewarePath("/a/b"))
    assert not path.startswith(ASGIMiddlewarePath("/a/b/c/e"))
    assert not path.startswith(ASGIMiddlewarePath("/x"))


@pytest.mark.asyncio
async def test_accessible():
    this_file = Path(__file__).resolve().as_posix()
    assert await ASGIMiddlewarePath(this_file).accessible()
