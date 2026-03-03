import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
#
from contextlib import asynccontextmanager
#
from app.base.exception.handle import AppException, ExceptionHandler
from app.base.middleware.apps import app_start_event, http_start_event, app_shutdown_event
#
from app.http.demo.ctrl import SampleCtrl as DemoSample
from app.http.demo_mg.ctrl import SampleCtrl as DemoMgSample
from app.http.chat.ctrl import BotCtrl


# 框架事件
@asynccontextmanager
async def lifespan(application: FastAPI):
    # 框架事件-应用启动
    await app_start_event(application)
    # 程序切换
    yield
    # 框架事件-应用关闭
    await app_shutdown_event(application)


"""框架主体"""
app = FastAPI(lifespan=lifespan)

"""跨域设置"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 框架事件-网路请求
@app.middleware("http")
async def http_start(request: Request, call_next):
    return await http_start_event(request, call_next)


# 业务异常拦截
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return ExceptionHandler().app_exception(request, exc)


# http异常拦截
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return ExceptionHandler().http_exception(request, exc)


# 验证器异常拦截
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return ExceptionHandler().validation_exception(request, exc)


@app.get("/")
def home():
    """无页面显示"""

    # 主动抛出异常
    raise AppException(code=1000, message="test unicornException")

    return "HOME"


"""demo示例模块路由"""
app.include_router(DemoSample.router, prefix="/demo")
"""demo-mongo示例模块路由"""
app.include_router(DemoMgSample.router, prefix="/demo_mg")
"""chat模块路由"""
app.include_router(BotCtrl.router, prefix="/chat")

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=False)
