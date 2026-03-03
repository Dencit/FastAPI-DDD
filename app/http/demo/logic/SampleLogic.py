from extend.match_ql.match_query import MatchQuery
from app.domain.demo.repo import SampleRepo


def save(request_input):
    data = SampleRepo.save(request_input)
    return data


def update(id, request_input):
    data = SampleRepo.update(id, request_input)
    return data


def delete(id, request_input: dict = None):
    data = SampleRepo.delete(id, request_input)
    return data


def read(all_request_query, request_query=None) -> tuple[any, any]:
    # 主表筛选逻辑 - 获取query查询表达式参数
    match_query = MatchQuery(all_request_query)
    # 检查查询参数存在 - 无则返回None
    if len(match_query.query_exist()) == 0:
        return None, None

    # 自动识别查询 - 返回模型实例
    data = SampleRepo.read(match_query)

    return data, None


def index(all_request_query, request_query=None) -> tuple[any, any]:
    # 主表筛选逻辑 - 获取query查询表达式参数
    match_query = MatchQuery(all_request_query)

    # 自动识别查询 - 返回模型实例
    data, metas = SampleRepo.index(match_query)

    return data, metas
