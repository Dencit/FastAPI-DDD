import re
import copy
from bson import ObjectId
#
from extend.convert.dicts import DictFormat


class MatchQuery(object):
    query_dict = dict

    # 实例设置
    def __init__(self, request_query):
        self.query_dict = request_query

    # 单例
    def __call__(self, *args, **kwargs):
        return self

    # 检查查询参数存在
    def query_exist(self):
        # 合并 默认 排除字段
        out_query_tup = (
            "_pagination", "_page", "_page_size",
            "_where", "_where_in", "where_in_sort", "_include", "_extend", "_search",
            "_sort", "_group", "_time",
        )
        # 执行过滤
        query_dict = DictFormat().diff_key(self.query_dict, out_query_tup)
        return query_dict

    # 查询动作标记
    def search_action(self):
        action = "default"
        query_dict = self.query_dict
        if len(query_dict) != 0 and query_dict.get("_search"):
            action = self.query_dict["_search"]
            print("action::", action)  #
        return action

    # 截取关联查询标记
    def include(self):
        include_list = []
        query_dict = self.query_dict
        if len(query_dict) != 0 and query_dict.get("_include"):
            include_str = query_dict.get("_include")
            include_list = include_str.split(",")
            print("include_list::", include_list)  #
        return include_list

    # 截取扩展查询标记
    def extend(self):
        extend_list = []
        query_dict = self.query_dict
        if len(query_dict) != 0 and query_dict.get("_extend"):
            extend_str = query_dict.get("_extend")
            extend_list = extend_str.split(",")
            print("extend_list::", extend_list)  #
        return extend_list

    # 截取筛选参数列表-db专用
    def search(self, struct, rule, filter_list: list):
        search_list = []

        def callback(key, ope, value):
            if ope == "=":
                search_list.append(getattr(struct, key) == value)
            if ope == "LIKE":
                value = "%" + value + "%"
                search_list.append(getattr(struct, key).like(value))
            if ope == "LIKE_START":
                value = value + "%"
                search_list.append(getattr(struct, key).like(value))
            if ope == "LIKE_END":
                value = "%" + value
                search_list.append(getattr(struct, key).like(value))
            if ope == "IN":
                search_list.append(getattr(struct, key).in_(value))

        self.search_call(rule, filter_list, callback)

        return search_list

    # 截取筛选参数列表-mongo专用
    def search_mg(self, rule, filter_list: list):
        search_dict = {}

        def callback(key, ope, value):
            if ope == "=":
                if key == "_id":
                    value = ObjectId(value)
                search_dict[key] = value
            if ope == "LIKE":
                search_dict[key] = {"$regex": value}
            if ope == "LIKE_START":
                search_dict[key] = {"$regex": '^' + value}
            if ope == "LIKE_END":
                search_dict[key] = {"$regex": value + '$'}
            if ope == "IN":
                values = []
                if key == "_id":
                    for val in copy.copy(value):
                        values.append(ObjectId(val))
                else:
                    values = value
                search_dict[key] = {"$in": values}

        self.search_call(rule, filter_list, callback)

        return search_dict

    # 截取筛选参数列表-闭包
    @staticmethod
    def __search_callback(key, ope, value):
        pass

    # 截取筛选参数列表-闭包
    def search_call(self, rule, filter_list: list, callback: __search_callback = None):
        # 返回结构
        search_list = []
        # 合并 默认 排除字段
        out_query_list = [
            "_pagination", "_page", "_page_size",
            "_where", "_where_in", "where_in_sort", "_include", "_extend", "_search",
            "_sort", "_group", "_time",
        ]
        # 合并 默认 和 自定义 排除字段
        merged_list = out_query_list + filter_list
        # print("merged_list::", merged_list) #
        # 执行过滤
        query_list = DictFormat().diff_key(self.query_dict, merged_list)
        # print("query_list::", query_list)  #
        if len(query_list) != 0:
            for key, value in query_list.items():
                operator = "="
                if DictFormat().is_set(rule, key):
                    operator = rule[key]
                # 筛选运算符预处理
                key, ope, value = self.search_operator(key, operator, value)
                # print("key, ope, value::", key, ope, value)  #
                if callback:
                    callback(key, ope, value)
        pass

    # 筛选运算符预处理
    def search_operator(self, key, operator, value):
        # 暂存字段名
        key_tmp = key
        # 排除符号:,%*
        value = str(value)
        value_tmp = re.compile(r"(,|\%|\*)").sub("", value)
        #
        if operator == "like":  # 模糊筛选处理
            match_l = re.compile(r"^(\%|\*).*").match(value)
            match_r = re.compile(r".*(\%|\*)$").match(value)
            if match_l:
                operator = "LIKE_END"
                # value = "%" + value_tmp
                value = value_tmp
            if match_r:
                operator = "LIKE_START"
                # value = value_tmp + "%"
                value = value_tmp
            if match_l and match_r:
                operator = "LIKE"
                # value = "%" + value_tmp + "%"
                value = value_tmp

        #
        if operator == "=":
            reg = re.compile(r"(,|\%|\*)")
            match = reg.findall(value)
            # print("match::", match)  #
            if len(match) != 0:
                if match[0] == ",":
                    operator = "IN"
                    value = value.split(",")
                if match[0] == "%" or match[0] == "*":
                    match_l = re.compile(r"^(\%|\*).*").match(value)
                    match_r = re.compile(r".*(\%|\*)$").match(value)
                    if match_l:
                        operator = "LIKE_END"
                        # value = "%" + value_tmp
                        value = value_tmp
                    if match_r:
                        operator = "LIKE_START"
                        # value = value_tmp + "%"
                        value = value_tmp
                    if match_l and match_r:
                        operator = "LIKE"
                        # value = "%" + value_tmp + "%"
                        value = value_tmp
            else:
                value = value_tmp

        return key, operator, value

    # 排序-sort参数转换-db专用
    def sort(self, struct):
        sort_list = []
        query_dict = self.query_dict
        if len(query_dict) != 0 and query_dict.get("_sort"):
            sort_str = query_dict["_sort"]
            sort_tup = sort_str.split(",")
            for key in sort_tup:
                reg = re.compile(r"^(-)")
                match = reg.match(key)
                if match:
                    key = reg.sub("", key)
                    sort_list.append(getattr(struct, key).desc())
                else:
                    sort_list.append(getattr(struct, key).asc())

            print("sort_list::", sort_list)  #
        return sort_list

    # 排序-sort参数转换-mongo专用
    def sort_mg(self):
        sort_list = []
        query_dict = self.query_dict
        if len(query_dict) != 0 and query_dict.get("_sort"):
            sort_str = query_dict["_sort"]
            sort_tup = sort_str.split(",")
            for key in sort_tup:
                reg = re.compile(r"^(-)")
                match = reg.match(key)
                if match:
                    key = reg.sub("", key)
                    sort_list.append((key, -1))
                else:
                    sort_list.append((key, 1))

            print("sort_list::", sort_list)  #
        return sort_list

    # 翻页处理
    def pagination(self):
        query_dict = self.query_dict
        # 默认值
        pagination = False
        page = 1
        page_size = 20
        # 获取参数
        if query_dict.get("_pagination") is None or query_dict.get("_pagination") != "false":
            pagination = True
            if query_dict.get("_page"):
                page = int(query_dict.get("_page"))
            if query_dict.get("_page_size"):
                page_size = int(query_dict.get("_page_size"))
        # 限制范围
        if page < 1:
            page = 1
        if page_size > 100:
            page_size = 100
        offset = (page - 1) * page_size
        # meta结构
        meta_dict = dict(
            pagination=pagination,
            page=page,
            page_size=page_size,
            offset=offset,
            page_total=0,
            total=0
        )
        print("meta_dict::", meta_dict)  #
        return meta_dict
