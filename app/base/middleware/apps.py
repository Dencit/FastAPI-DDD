import time
from fastapi import FastAPI, Request


# 框架事件-应用启动
async def app_start_event(app: FastAPI):
    """https://fastapi.tiangolo.com/zh/advanced/events/#_5"""
    print("[APP START]")


# 框架事件-网路请求
async def http_start_event(request: Request, call_next):
    """https://fastapi.tiangolo.com/zh/tutorial/middleware/#_2"""
    print("[HTTP START]")
    #
    start_time = time.perf_counter()
    process_time = time.perf_counter() - start_time
    #
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 框架事件-应用关闭
async def app_shutdown_event(app: FastAPI):
    """https://fastapi.tiangolo.com/zh/advanced/events/#_5"""
    print("[APP END]")
