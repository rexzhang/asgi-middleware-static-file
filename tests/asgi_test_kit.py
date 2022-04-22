from base64 import b64encode
from dataclasses import dataclass
from typing import Union

import pytest
from icecream import ic

# from:
#  - https://gist.github.com/rexzhang/40e7f5ba023ec16fde860509eb9f3253
# python version:
#  - 3.6+
# example:
#  - middleware:
#   - https://github.com/rexzhang/asgi-webdav/blob/main/tests/test_middleware_cors.py

MOCK_APP_RESPONSE_SUCCESS = "I'm mock App"


class ASGIApp:
    def __init__(
        self,
        response_text: str = MOCK_APP_RESPONSE_SUCCESS,
        app_response_header: Union[dict[str, str], None] = None,
    ):
        self.response_body = response_text.encode("utf-8")
        self.app_response_header = app_response_header

    async def __call__(self, scope, receive, send):
        scope_type = scope.get("type")
        if scope_type == "http":
            return await self._type_http(scope, receive, send)

        elif scope_type == "websocket":
            return await self._type_websocket(scope, receive, send)

        else:
            raise Exception("type is not http or websocket")

    async def _type_http(self, scope, receive, send):
        headers = {"Content-Type": "text/plain"}
        if self.app_response_header is not None:
            headers.update(self.app_response_header)

        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (k.encode("utf-8"), v.encode("utf-8")) for k, v in headers.items()
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": self.response_body,
            }
        )

    async def _type_websocket(self, scope, receive, send):
        # TODO !!!
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [],
            }
        )


@dataclass
class ASGIRequest:
    type: str
    method: str
    path: str
    headers: dict[str, str]
    data: bytes

    def get_scope(self):
        return {
            "type": self.type,
            "method": self.method,
            "headers": [
                (item[0].lower().encode("utf-8"), item[1].encode("utf-8"))
                for item in self.headers.items()
            ],
            "path": self.path,
        }


@dataclass
class ASGIResponse:
    status_code: Union[int, None] = None
    _headers: Union[dict[str, str], None] = None
    data: Union[bytes, None] = None

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @headers.setter
    def headers(self, data: list[tuple[bytes, bytes]]):
        ic("header in respone", data)
        self._headers = dict()
        try:
            for k, v in data:
                if isinstance(k, bytes):
                    k = k.decode("utf-8")
                else:
                    raise Exception("type(Key:{}) isn't bytes: {}".format(k, data))
                if isinstance(v, bytes):
                    v = v.decode("utf-8")
                else:
                    raise Exception("type(Value:{}) isn't bytes: {}".format(v, data))

                self._headers[k.lower()] = v
        except ValueError as e:
            raise ValueError(e, data)

    @property
    def text(self) -> str:
        return self.data.decode("utf-8")


class ASGITestClient:
    request: ASGIRequest
    response: ASGIResponse

    def __init__(
        self,
        app,
    ):
        self.app = app

    async def _fake_receive(self):
        return self.request.data

    async def _fake_send(self, data: dict):
        data_type = data.get("type")
        if data_type == "http.response.start":
            self.response.status_code = data["status"]
            self.response.headers = data["headers"]

        elif data_type == "http.response.body":
            self.response.data = data["body"]

        else:
            raise NotImplementedError()

        return

    async def _call_method(self) -> ASGIResponse:
        ic("input", self.request)
        headers = {
            "user-agent": "ASGITestClient",
        }
        headers.update(self.request.headers)
        self.request.headers = headers
        ic("prepare", self.request)

        self.response = ASGIResponse()
        await self.app(
            self.request.get_scope(),
            self._fake_receive,
            self._fake_send,
        )

        return self.response

    @staticmethod
    def create_basic_authorization_headers(
        username: str, password: str
    ) -> dict[str, str]:
        return {
            "authorization": "Basic {}".format(
                b64encode("{}:{}".format(username, password).encode("utf-8")).decode(
                    "utf-8"
                )
            )
        }

    async def websocket(self, path, headers: dict[str, str] = None) -> ASGIResponse:
        self.request = ASGIRequest("websocket", "GET", path, {}, b"")  # TODO
        return await self._call_method()

    async def get(self, path, headers: dict[str, str] = None) -> ASGIResponse:
        if headers is None:
            headers = dict()
        self.request = ASGIRequest("http", "GET", path, headers, b"")
        return await self._call_method()

    async def options(self, path, headers: dict[str, str]) -> ASGIResponse:
        self.request = ASGIRequest("http", "OPTIONS", path, headers, b"")
        return await self._call_method()


@pytest.mark.asyncio
async def test_base():
    client = ASGITestClient(ASGIApp())
    response = await client.get("/")
    assert response.status_code == 200
