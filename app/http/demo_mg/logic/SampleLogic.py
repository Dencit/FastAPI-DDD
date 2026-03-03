from extend.match_ql.match_query import MatchQuery
from app.domain.demo_mg.repo import SampleRepo


def save(request_input):
    result = SampleRepo.save(request_input)
    return result


def update(id, request_input):
    result = SampleRepo.update(id, request_input)
    return result


def delete(id, request_input: dict = None):
    result = SampleRepo.delete(id, request_input)
    return result


def read(all_request_query, request_query=None) -> tuple[any, any]:
    # 主表筛选逻辑 - 获取query查询表达式参数
    match_query = MatchQuery(all_request_query)
    # 检查查询参数存在 - 无则返回None
    if len(match_query.query_exist()) == 0:
        return None, None
    #
    data, meta = SampleRepo.read(match_query, request_query)
    return data, meta


def index(all_request_query, request_query=None) -> tuple[any, any]:
    # 主表筛选逻辑 - 获取query查询表达式参数
    match_query = MatchQuery(all_request_query)
    # 检查查询参数存在 - 无则返回None
    if len(match_query.query_exist()) == 0:
        return None, None
    #
    data, meta = SampleRepo.index(match_query, request_query)
    return data, meta
