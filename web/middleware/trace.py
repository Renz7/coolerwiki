# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/27 17:07
"""
import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class TraceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, debug: bool = False) -> None:
        super().__init__(app)
        self.debug = debug

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self.debug:
            start = time.perf_counter()
            path = request.url.path
            resp = await call_next(request)
            end = time.perf_counter()
            logger.info("response '{}' in {} seconds", path, end - start)
            return resp
        else:
            return await call_next(request)
