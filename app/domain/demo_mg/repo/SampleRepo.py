from extend.match_ql.match_query import MatchQuery
from extend.mdb.mdb import Mdb
from bson import ObjectId

mg_db = "admin"
mg_collect = "sample"


def save(request_input) -> object:
    collect = Mdb().collect(mg_db, mg_collect)
    data = collect.insert_one(request_input)
    if data.inserted_id:
        request_input["_id"] = str(data.inserted_id)
    return request_input


def update(id, request_input) -> object:
    collect = Mdb().collect(mg_db, mg_collect)
    # 查询文档id
    query = {"_id": ObjectId(id)}
    result = collect.find_one(query)
    # 根据文档id 更新数据
    up_data = {
        "$set": request_input
    }
    data = collect.update_one(query, up_data)
    if data:
        request_input["_id"] = id

    return request_input


def delete(id, request_input: dict = None) -> object:
    collect = Mdb().collect(mg_db, mg_collect)
    # 查询文档id
    query = {"_id": ObjectId(id)}
    result = collect.find_one(query)
    print("result::", result)
    # 根据文档id 删除数据
    collect.delete_one(query)

    return {"_id": id}


def read(match_query: MatchQuery, request_query):
    # mongodb 连接
    collect = Mdb().collect(mg_db, mg_collect)

    """根据 ?_search=default 参数, 切换 捕捉到 ?type=1&status=1 ...的值的运算符."""
    rule = {}
    action = match_query.search_action()
    if action == "default":
        rule["id"] = "="
        # rule["name"] = "like"

    """捕捉 ?type = 1 & status = 1...的值, 转化成查询数组"""
    filter_dict = []  # 排除筛选key
    where_list = match_query.search_mg(rule, filter_dict)
    print("where_list::", where_list)

    # 执行查询
    data = collect.find_one(where_list)
    if data:
        data["_id"] = str(data["_id"])

    return data, None


def index(match_query: MatchQuery, request_query):
    # mongodb 连接
    collect = Mdb().collect(mg_db, mg_collect)

    """根据 ?_search=default 参数, 切换 捕捉到 ?type=1&status=1 ...的值的运算符."""
    rule = {}
    action = match_query.search_action()
    if action == "default":
        rule["id"] = "="
        # rule["name"] = "like"

    """捕捉 ?type = 1 & status = 1...的值, 转化成查询数组"""
    filter_dict = []  # 排除筛选key
    where_list = match_query.search_mg(rule, filter_dict)
    print("where_list::", where_list)

    """?_sort = -id"""
    order_list = match_query.sort_mg()
    print("order_list::", order_list)

    """?_pagination = true 翻页"""
    metas = match_query.pagination()
    start_row = (metas['page'] - 1) * metas['page_size']
    # end_row = metas['page'] * metas['page_size']

    """合计"""
    counts = collect.count_documents(where_list)
    metas['total'] = counts
    metas['total_page'] = int(counts / metas['page_size'])

    # 执行查询
    results = collect.find(where_list).skip(start_row).limit(metas['page_size']).sort(order_list)

    datas = []
    for item in results:
        item["_id"] = str(item["_id"])
        datas.append(item)

    return datas, metas
