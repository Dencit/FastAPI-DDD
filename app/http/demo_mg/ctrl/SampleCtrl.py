from fastapi import APIRouter, Request, Query, Depends
from typing import Annotated
#
from app.base.middleware.routes import open_auth
from app.base.request.http_request import HttpRequest
from app.base.respond.http_respond import HttpRespond
from app.http.demo_mg.request import SampleRequest
from app.http.demo_mg.logic import SampleLogic
from extend.api_cache.api_cache import ApiCache

# 路由组
router = APIRouter()


@router.post(path="/sample/save")
async def sample_save(request_input: SampleRequest.Save, auth: dict = Depends(open_auth)):
    """新增行"""
    print("auth::", auth)
    # 输入
    request_input = request_input.dict(exclude_none=True)

    # 业务逻辑
    data = SampleLogic.save(request_input)

    # 标准输出
    return HttpRespond().save(data)


@router.put(path="/sample/update/{id}")
async def sample_update(request_input: SampleRequest.Update, id: str, auth: dict = Depends(open_auth)):
    """更新行"""
    print("auth::", auth)
    # 输入
    request_input = request_input.dict(exclude_none=True)

    # 业务逻辑
    data = SampleLogic.update(id, request_input)

    # 标准输出
    return HttpRespond().update(data)


@router.delete(path="/sample/delete/{id}")
async def sample_delete(id: str, auth: dict = Depends(open_auth)):
    """删除行"""
    print("auth::", auth)

    # 业务逻辑
    data = SampleLogic.delete(id)

    # 标准输出
    return HttpRespond().delete(data)


@router.get(path="/sample/read")
async def sample_read(request: Request, request_query: Annotated[SampleRequest.Read, Query()], auth: dict = Depends(open_auth)):
    """获取行"""
    print("auth::", auth)

    # 输入
    all_request_query = HttpRequest().query_to_dict(request)
    request_query = request_query.dict(exclude_none=True)

    # 检查url参数缓存
    api_cache = ApiCache(all_request_query)
    hkey = api_cache.hkey_by_class_method("sample@read")
    query_key = api_cache.query_key_by_request(all_request_query)
    # query_key += "&id=" + request_query["id"]

    # 缓存闭包
    def callback():
        # 业务逻辑
        result, metas = SampleLogic.read(all_request_query, request_query)
        return result, metas

    data, meta = api_cache.collect(hkey, query_key, callback, 0)

    # 标准输出
    return HttpRespond().read(data, None)


@router.get(path="/sample/index")
async def sample_index(request: Request, request_query: Annotated[SampleRequest.Index, Query()], auth: dict = Depends(open_auth)):
    """获取列表"""
    print("auth::", auth)
    # 输入
    all_request_query = HttpRequest().query_to_dict(request)
    request_query = request_query.dict(exclude_none=True)

    # 检查url参数缓存
    api_cache = ApiCache(all_request_query)
    hkey = api_cache.hkey_by_class_method("sample@index")
    query_key = api_cache.query_key_by_request(all_request_query)

    # 缓存闭包
    def callback():
        # 业务逻辑
        result, metas = SampleLogic.index(all_request_query, request_query)
        return result, metas

    data, meta = api_cache.collect(hkey, query_key, callback, 0)

    return HttpRespond().index(data, meta)
