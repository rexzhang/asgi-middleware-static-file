import mimetypes
import os
from datetime import datetime
from hashlib import md5
from os import PathLike
from pathlib import Path
from typing import Callable, List, Optional, Union

import aiofiles
import aiofiles.os
import aiofiles.ospath

_FILE_BLOCK_SIZE = 64 * 1024


class ASGIMiddlewarePath:
    def __init__(self, path: Union[PathLike, str]):
        if not isinstance(path, Path):
            path = Path(path)

        self.path = path.resolve()
        self.path_as_str = self.path.as_posix()
        self.parts = self.path.parts
        self.count = len(self.parts)

    def join_path(self, path: Union[PathLike, str]) -> "ASGIMiddlewarePath":
        return ASGIMiddlewarePath(self.path.joinpath(path))

    def startswith(self, path: "ASGIMiddlewarePath") -> bool:
        return self.parts[: path.count] == path.parts

    async def accessible(self) -> bool:
        if await aiofiles.ospath.isfile(self.path) and await aiofiles.os.access(
            self.path, os.R_OK
        ):
            return True

        return False


class ASGIMiddlewareStaticFile:
    def __init__(
        self, app, static_url: str, static_root_paths: List[Union[PathLike, str]]
    ) -> None:
        self.app = app

        static_url = static_url.strip("/").rstrip("/")
        if len(static_url) == 0:
            self.static_url = "/"
        else:
            self.static_url = f"/{static_url}/"

        self.static_url_length = len(self.static_url)
        self.static_root_paths = [ASGIMiddlewarePath(p) for p in static_root_paths]

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        s_path = scope.get("path")
        if s_path is None or s_path[: self.static_url_length] != self.static_url:
            await self.app(scope, receive, send)
            return

        if scope["method"] == "HEAD":  # TODO
            await self._handle(send, s_path[self.static_url_length :], is_head=True)
            return

        elif scope["method"] == "GET":
            await self._handle(send, s_path[self.static_url_length :])
            return

        else:
            # 405
            await self.send_response_in_one_call(send, 405, b"405 METHOD NOT ALLOWED")
            return

    async def _handle(self, send, sub_path, is_head=False) -> None:
        # search file
        try:
            abs_path = await self.locate_the_file(sub_path)
        except ValueError:
            await self.send_response_in_one_call(
                send, 403, b"403 FORBIDDEN, CROSS BORDER ACCESS"
            )
            return

        if abs_path is None:
            await self.send_response_in_one_call(send, 404, b"404 NOT FOUND")
            return

        # create headers
        content_type, encoding = mimetypes.guess_type(abs_path)
        if content_type is None:
            content_type = b""
        else:
            content_type = content_type.encode("utf-8")
        if encoding is None:
            encoding = b""
        else:
            encoding = encoding.encode("utf-8")
        stat_result = await aiofiles.os.stat(abs_path)
        file_size = str(stat_result.st_size).encode("utf-8")
        last_modified = (
            datetime.fromtimestamp(stat_result.st_mtime)
            .strftime("%a, %d %b %Y %H:%M:%S GMT")
            .encode("utf-8")
        )
        headers = [
            (b"Content-Encodings", encoding),
            (b"Content-Type", content_type),
            (b"Content-Length", file_size),
            (b"Accept-Ranges", b"bytes"),
            (b"Last-Modified", last_modified),
            (b"ETag", md5(file_size + last_modified).hexdigest().encode("utf-8")),
        ]

        # send headers
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": headers,
            }
        )
        if is_head:
            await send(
                {
                    "type": "http.response.body",
                }
            )

            return

        # send file
        async with aiofiles.open(abs_path, mode="rb") as f:
            more_body = True
            while more_body:
                data = await f.read(_FILE_BLOCK_SIZE)
                more_body = len(data) == _FILE_BLOCK_SIZE
                await send(
                    {
                        "type": "http.response.body",
                        "body": data,
                        "more_body": more_body,
                    }
                )

        return

    async def locate_the_file(self, sub_path: Union[PathLike, str]) -> Optional[str]:
        """location the file in self.static_root_paths"""
        for root_path in self.static_root_paths:
            abs_path = root_path.join_path(sub_path)
            if not abs_path.startswith(root_path):
                raise ValueError

            if await abs_path.accessible():
                return abs_path.path_as_str

        return None

    @staticmethod
    async def send_response_in_one_call(
        send: Callable, status: int, message: bytes
    ) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [(b"Content-Type", b"text/plain; UTF-8")],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": message,
            }
        )
        return
