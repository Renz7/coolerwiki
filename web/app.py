# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/27 16:47
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from web.middleware.trace import TraceMiddleware
from web.routers import routers

origins = ['*']


def create_app(debug=False):
    app = FastAPI(debug=debug,
                  title="cooler.wiki",
                  )
    app.add_middleware(
        CORSMiddleware,
        # 允许跨域的源列表
        allow_origins=origins,
        # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
        allow_credentials=True,
        # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
        allow_methods=["*"],
        # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
        # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
        allow_headers=["*"],
        # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
        # expose_headers=["*"]
        # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
        # max_age=1000
    )
    app.add_middleware(TraceMiddleware, debug=debug)

    for router in routers:
        app.include_router(router)

    @app.get("/health")
    def health_check():
        return "I'm healthy"

    return app


app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get("DEBUG", default='false') == "true"
    logger.info("Start with Debug Mode:{}", debug_mode)
    uvicorn.Server(uvicorn.Config(
        create_app(debug_mode),
        reload=True
    )
    ).run()
