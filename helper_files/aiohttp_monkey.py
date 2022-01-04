# This is a monkey patch for aiohttp because it limits client response headers to 8190 Bytes.  GW2 api returns bad requests as 269s in the header, which quickly passes 8190 bytes

from typing import Optional

from aiohttp.client_exceptions import ClientPayloadError
from aiohttp.client_proto import ResponseHandler
from aiohttp.helpers import BaseTimerContext
from aiohttp.http import HttpResponseParser


def set_response_params(
    self,
    *,
    timer: Optional[BaseTimerContext] = None,
    skip_payload: bool = False,
    read_until_eof: bool = False,
    auto_decompress: bool = True,
    read_timeout: Optional[float] = None,
    read_bufsize: int = 2 ** 16
) -> None:
    self._skip_payload = skip_payload

    self._read_timeout = read_timeout
    self._reschedule_timeout()

    self._parser = HttpResponseParser(
        self,
        self._loop,
        read_bufsize,
        timer=timer,
        payload_exception=ClientPayloadError,
        response_with_body=not skip_payload,
        read_until_eof=read_until_eof,
        auto_decompress=auto_decompress,
        # These three lines are the important change
        max_line_size=8190 * 4,
        max_headers=32768 * 4,
        max_field_size=8190 * 4
    )

    if self._tail:
        data, self._tail = self._tail, b""
        self.data_received(data)


#ResponseHandler.set_response_params = set_response_params
