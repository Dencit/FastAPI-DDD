from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
# from starlette.responses import StreamingResponse
from qianfan import Qianfan
#
from app.base.middleware.routes import open_auth
from app.base.respond.http_respond import HttpRespond
from app.http.chat.request import BotRequest
from config.app import AppSettings
from extend.mdb.mdb import Mdb

# 路由组
router = APIRouter()


@router.post(path="/bot/save")
async def bot_save(request_input: BotRequest.Save, auth: dict = Depends(open_auth)):
    """新增行"""

    mdb = Mdb().client()
    dblist = mdb.list_database_names()
    print("dblist::", dblist)

    # 输入
    request_input = request_input.dict(exclude_none=True)
    messages = [request_input]

    qianfan = AppSettings().qianfan
    api_key = qianfan["api_key"]
    access_key = qianfan["access_key"]
    secret_key = qianfan["secret_key"]
    client = Qianfan(api_key=api_key, access_key=access_key, secret_key=secret_key)
    completion = client.chat.completions.create(model="deepseek-v3", messages=messages)
    res = completion.choices[0]

    data = {
        "chat/bot/save": "ok",
        "res": res
    }

    # 标准输出
    return HttpRespond().save(data)


@router.post(path="/bot/stream")
async def bot_stream(request_input: BotRequest.Save, auth: dict = Depends(open_auth)):
    # 输入
    request_input = request_input.dict(exclude_none=True)
    messages = [request_input]

    qianfan = AppSettings().qianfan
    api_key = qianfan["api_key"]
    access_key = qianfan["access_key"]
    secret_key = qianfan["secret_key"]
    client = Qianfan(api_key=api_key, access_key=access_key, secret_key=secret_key)
    completion = client.chat.completions.create(model="deepseek-r1", messages=messages, stream=True)

    def handle_post_request():
        for r in completion:
            info = ""
            reasoning_content = r.choices[0].delta.reasoning_content
            content = r.choices[0].delta.content
            if reasoning_content is not None:
                info = reasoning_content
                print(">", info)
            if content is not None:
                info = content
                print("|", info)
            yield info

    return StreamingResponse(handle_post_request())
