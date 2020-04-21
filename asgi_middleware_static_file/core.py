#!/usr/bin/env python
# coding=utf-8


import os
import mimetypes
from datetime import datetime
from hashlib import md5

import aiofiles
from aiofiles.os import stat as aio_stat

_FILE_BLOCK_SIZE = 64 * 1024


class ASGIMiddlewareStaticFile:
    def __init__(self, app, static_url, static_paths) -> None:
        self.app = app
        self.static_url = '/{}/'.format(static_url.strip('/').rstrip('/'))
        self.static_url_length = len(self.static_url)
        self.static_paths = static_paths

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "http" and scope['path'][:self.static_url_length] == self.static_url:
            if scope['method'] == 'GET':
                await self.handle(send, scope['path'][self.static_url_length:])
                return

            elif scope['method'] == 'HEAD':  # TODO
                await self.handle(send, scope['path'][self.static_url_length:], is_head=True)
                return

            # 405
            await self._send_unusual_response(send, 405, b'405 METHOD NOT ALLOWED')
            return

        await self.app(scope, receive, send)
        return

    async def handle(self, send, filename, is_head=False) -> None:
        # search file
        absolute_path_file_name = await self._search_file(self.static_paths, filename)
        if absolute_path_file_name is None:
            # 404
            await self._send_unusual_response(send, 404, b'404 NOT FOUND')
            return

        # create headers
        content_type, encoding = mimetypes.guess_type(absolute_path_file_name)
        if content_type:
            content_type = bytes(content_type, encoding='utf-8')
        else:
            content_type = b''
        if encoding:
            encoding = bytes(encoding, encoding='utf-8')
        else:
            encoding = b''
        stat_result = await aio_stat(absolute_path_file_name)
        file_size = bytes(str(stat_result.st_size), encoding='utf-8')
        last_modified = bytes(datetime.fromtimestamp(stat_result.st_mtime).strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        ), encoding='utf-8')
        headers = [
            (b'Content-Encodings', encoding),
            (b'Content-Type', content_type),
            (b'Content-Length', file_size),
            (b'Accept-Ranges', b'bytes'),
            (b'Last-Modified', last_modified),
            (b'ETag', md5(file_size + last_modified).hexdigest().encode('utf-8')),
        ]

        # send headers
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': headers,
        })
        if is_head:
            await send({
                'type': 'http.response.body',
            })

            return

        # send file
        async with aiofiles.open(absolute_path_file_name, mode="rb") as f:
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

    @staticmethod
    async def _search_file(search_paths, filename):
        for path in search_paths:
            f_name = os.path.join(path, filename)
            if os.path.exists(f_name) and os.path.isfile(f_name) and os.access(f_name, os.R_OK):
                return f_name

        return None

    @staticmethod
    async def _send_unusual_response(send, status, message) -> None:
        await send({
            'type': 'http.response.start',
            'status': status,
            'headers': [(b'Content-Type', b'text/plain; UTF-8')],
        })

        await send({
            'type': 'http.response.body',
            'body': message,
        })
        return
