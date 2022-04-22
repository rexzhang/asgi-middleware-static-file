from asgi_middleware_static_file import ASGIMiddlewareStaticFile


def test_param_parser_static_url():
    m = ASGIMiddlewareStaticFile(app=None, static_url="", static_root_paths=[])
    assert m.static_url == "/"

    m = ASGIMiddlewareStaticFile(app=None, static_url="/", static_root_paths=[])
    assert m.static_url == "/"

    m = ASGIMiddlewareStaticFile(app=None, static_url="/a", static_root_paths=[])
    assert m.static_url == "/a/"

    m = ASGIMiddlewareStaticFile(app=None, static_url="/a/", static_root_paths=[])
    assert m.static_url == "/a/"
