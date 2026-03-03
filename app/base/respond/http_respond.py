from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class HttpRespond(object):

    # 新增数据结果返回
    def save(self, data, metas: dict = None) -> object:
        return self.respond(data, metas, status.HTTP_201_CREATED)

    # 更新数据结果返回
    def update(self, data, metas: dict = None) -> object:
        return self.respond(data, metas, status.HTTP_202_ACCEPTED)

    # 删除数据结果返回
    def delete(self, data, metas: dict = None) -> object:
        return self.respond(data, metas, status.HTTP_202_ACCEPTED)

    # 输出单行数组
    def read(self, data, metas: dict = None) -> object:
        return self.respond(data, metas, status.HTTP_200_OK)

    # 输出多行数组
    def index(self, data, metas: dict = None) -> object:
        return self.respond_collect(data, metas, status.HTTP_200_OK)

    # 一般输出
    def respond(self, data, metas: dict = None, status_code: int = None) -> object:
        res_data = None
        if data is not None:
            res_data = data

        respond_tmp = dict()
        respond_tmp["code"] = 0
        respond_tmp["message"] = "success"
        respond_tmp["data"] = res_data
        respond_tmp["meta"] = metas
        respond_obj = jsonable_encoder(respond_tmp)
        return JSONResponse(status_code=status_code, content=respond_obj)

    # 多行输出+meta
    def respond_collect(self, data, metas: dict = None, status_code: int = None) -> object:
        res_data = None
        if data is not None:
            res_data = data

        respond_tmp = dict()
        respond_tmp["code"] = 0
        respond_tmp["message"] = "success"
        respond_tmp["data"] = res_data
        respond_tmp["meta"] = metas
        respond_obj = jsonable_encoder(respond_tmp)
        return JSONResponse(status_code=status_code, content=respond_obj)
