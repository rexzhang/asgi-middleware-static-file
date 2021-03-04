import pathlib
from pathlib import Path

import pytest

from asgi_middleware_static_file import ASGIMiddlewareStaticFile, Path

BASE_PATH = pathlib.Path(__name__).parent.joinpath('demo_static').resolve()


@pytest.mark.asyncio
async def test_cross_border_access():
    print(BASE_PATH)
    mw = ASGIMiddlewareStaticFile(None, 'static', [BASE_PATH])

    assert isinstance(mw.locate_the_file('DEMO'), Path)
    assert mw.locate_the_file('not_found') is None

    with pytest.raises(ValueError):
        mw.locate_the_file('../setup.py')
