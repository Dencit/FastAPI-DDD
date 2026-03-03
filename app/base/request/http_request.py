from fastapi import Request
from starlette.datastructures import QueryParams
from extend.convert import values


class HttpRequest(object):

    # 转换 字符串form 为 字典
    def form_to_dict(self, request: Request):
        temp_dict = dict()
        if len(request) > 0:
            list_first = request.split("&")
            if len(list_first) > 0:
                for item in list_first:
                    item_list = item.split("=")
                    # 判断字符串是否数字
                    val = item_list[1]
                    if val.isdigit():
                        val = int(val)
                    else:
                        if values.is_float(val) is True:
                            val = float(val)

                    temp_dict[item_list[0]] = val
        return temp_dict

    # 转换 Request 所有参数, 包括特殊key参数.
    def query_to_dict(self, request: Request):
        temp_dict = dict()
        if len(request) > 0:
            query_params = QueryParams(request.query_params)
            for key, val in query_params.items():
                if val.isdigit():
                    val = int(val)
                else:
                    if values.is_float(val) is True:
                        val = float(val)
                temp_dict[key] = val
        return temp_dict
