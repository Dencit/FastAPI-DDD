from functools import lru_cache


@lru_cache
class BaseErr(object):
    # 系统码
    VALIDATION_ERROR = {"code": 1026, "msg": "输入参数有误"}
    # 全局 - 公共业务码
    AUTH_MUST = {"code": 100000, "msg": "访问必须授权"}
    SAVE_FAIL = {"code": 100011, "msg": "数据新增失败"}
    UPDATE_FAIL = {"code": 100012, "msg": "数据更新失败"}
    DELETE_FAIL = {"code": 100013, "msg": "数据删除失败"}
    ID_IS_NOT_EXIST = {"code": 100014, "msg": "ID 不存在"}
    ID_IS_EXIST = {"code": 100015, "msg": "ID 已存在"}
