from datetime import datetime
#
from app.base.exception.handle import AppException
from extend.db.db import Db
from app.domain.demo.entity import SampleEntity
from app.base.err.base_err import BaseErr
from app.domain.demo.err.demo_err import DemoErr

"""sqlalchemy 文档: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html"""
"""sqlalchemy 文档: https://zhuanlan.zhihu.com/p/676552345"""

# 数据库连接
orm = Db().get_session()


def save(request_input) -> object:
    result = None

    """输入转结构"""
    data_obj = SampleEntity.Sample(**request_input)
    """数据操作"""
    orm.add(data_obj)
    orm.commit()
    orm.refresh(data_obj)
    if type(data_obj) != "None":
        print("sample_save::", data_obj)
        result = data_obj

    return result


def update(id, request_input) -> object:
    result = dict()

    data_obj = orm.get(SampleEntity.Sample, id)
    # 不存在则拦截
    if data_obj is None:
        raise AppException(code=BaseErr.ID_IS_NOT_EXIST["code"], message=BaseErr.ID_IS_NOT_EXIST["msg"])

    for key, val in request_input.items():
        if getattr(data_obj, key) is not None:
            setattr(data_obj, key, val)
    orm.add(data_obj)
    orm.commit()
    orm.refresh(data_obj)

    print("sample_update::", data_obj)
    result = data_obj

    return result


def delete(id, request_input: dict = None) -> object:
    result = dict()

    data_obj = orm.get(SampleEntity.Sample, id)
    # 不存在则拦截
    if data_obj is None:
        raise AppException(code=DemoErr.ID_IS_NOT_EXIST["code"], message=DemoErr.ID_IS_NOT_EXIST["msg"])

    """软删除"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_obj.deleted_at = now_str
    orm.add(data_obj)
    """硬删除"""
    # session.delete(delete_obj)
    orm.commit()
    print("sample_delete::", data_obj)

    result["id"] = id

    return result


def read(match_query):
    """数据操作"""
    model = SampleEntity.Sample
    query_set = orm.query(model)

    """根据 ?_search=default 参数, 切换 捕捉到 ?type=1&status=1 ...的值的运算符."""
    rule = {}
    action = match_query.search_action()
    if action == "default":
        rule["id"] = "="
        # rule["name"] = "like"

    """捕捉 ?type = 1 & status = 1...的值, 转化成查询数组"""
    filter_tup = []  # 排除筛选key
    where_list = match_query.search(model, rule, filter_tup)
    query_set = query_set.filter(*where_list)

    """?_extend = user, info - 副表扩展查询标记."""
    extends = match_query.extend()
    if len(extends) != 0:
        print("extends::", extends)

    """只取一行"""
    query_set = query_set.offset(0).limit(1)
    result = query_set.all()
    print("sample_read::", result)

    """?_include = user, info - 副表关联模型, 用于数据输出, 不是查询条件."""
    includes = match_query.include()
    if len(includes) != 0:
        print("includes::", includes)
        for item in result:
            if 'user' in includes:
                getattr(item, "user")
            if 'users' in includes:
                getattr(item, "users")

    return result


def index(match_query):
    """数据操作"""
    model = SampleEntity.Sample
    query_set = orm.query(model)

    """根据 ?_search=default 参数, 切换 捕捉到 ?type=1&status=1 ...的值的运算符."""
    rule = {}
    action = match_query.search_action()
    if action == "default":
        rule["id"] = "="
        # rule["name"] = "like"

    """捕捉 ?type = 1 & status = 1...的值, 转化成查询数组"""
    filter_tup = []  # 排除筛选key
    where_list = match_query.search(model, rule, filter_tup)
    query_set = query_set.filter(*where_list)

    """?_extend = user, info - 副表扩展查询标记."""
    extends = match_query.extend()
    if len(extends) != 0:
        print("extends::", extends)

    """?_sort = -id"""
    order_list = match_query.sort(model)
    query_set = query_set.order_by(*order_list)

    """默认排序"""
    query_set = query_set.order_by(model.updated_at.desc())

    """?_pagination = true 翻页"""
    metas = match_query.pagination()
    start_row = (metas['page'] - 1) * metas['page_size']
    end_row = metas['page'] * metas['page_size']
    """合计"""
    counts = query_set.count()
    print("counts::", counts)
    if counts > 0:
        metas['total'] = counts
        metas['total_page'] = int(counts / metas['page_size'])
    """翻页"""
    query_set = query_set.offset(start_row).limit(end_row)
    result = query_set.all()
    print("sample_index::", result)

    """?_include = user, info - 副表关联模型, 用于数据输出, 不是查询条件."""
    includes = match_query.include()
    if len(includes) != 0:
        print("includes::", includes)
        for item in result:
            if 'user' in includes:
                getattr(item, "user")
            if 'users' in includes:
                getattr(item, "users")

    return result, metas
