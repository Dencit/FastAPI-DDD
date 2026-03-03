from functools import lru_cache


@lru_cache
class DemoErr(object):
    # 模块 - 公共业务码

    # 单元 - 模型业务码
    ID_IS_NOT_EXIST = {"code": 200001, "msg": "某某ID 不存在"}
    ID_IS_EXIST = {"code": 200002, "msg": "某某ID 已存在"}
