import time
from fastapi import FastAPI, Request, HTTPException


# 路由中间件 - 开放权限
async def open_auth(request: Request):
    token = request.headers.get("Authorization")
    print("on open_auth")
    if not token:
        raise HTTPException(400, "missing token header")
    return {"token": "abcdefg"}


# 路由中间件 - 用户权限
async def user_auth(request: Request):
    token = request.headers.get("Authorization")
    print("on user_auth")
    if not token:
        raise HTTPException(400, "missing token header")
    return {"token": "abcdefg"}
