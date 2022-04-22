from pathlib import Path

from asgi_middleware_static_file import ASGIMiddlewarePath

path = ASGIMiddlewarePath("/a/b/c/")


def test_joinpath():
    assert path.joinpath("d").path_as_str == "/a/b/c/d"
    assert path.joinpath("d/e").path_as_str == "/a/b/c/d/e"


def test_startswith():
    assert path.startswith(ASGIMiddlewarePath("/a/b"))
    assert not path.startswith(ASGIMiddlewarePath("/a/b/c/e"))
    assert not path.startswith(ASGIMiddlewarePath("/x"))


def test_accessible():
    this_file = Path(__file__).resolve().as_posix()
    assert ASGIMiddlewarePath(this_file).accessible()
