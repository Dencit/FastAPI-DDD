import json
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from extend.rdb.rdb import Rdb
from redis import Redis


class ApiCache(object):
    # 实例初始化
    def __init__(self, request_query: dict, select: int = 0):
        self.query: dict = request_query
        self.rdb: Redis = Rdb().client(select)

    # 生成哈希KEY - 通过类和函数
    def hkey_by_class_method(self, class_and_method: str) -> str:
        hkey = "api_cache:" + "_".join(class_and_method.split("\\"))
        return hkey

    # 生成 QUERY KEY/ HEADER KEY - 通过GET请求参数
    def query_key_by_request(self, request_query: dict) -> str:
        query_key = ""
        if len(request_query) > 0:
            # 对键进行排序
            sorted_keys = sorted(request_query.keys())
            for key in sorted_keys:
                value = request_query[key]
                # 不拼接缓存键
                if key != "_time":
                    query_key += f"&{key}={str(value)}"
            if query_key:  # 如果 query_key 不为空
                query_key = "/" + query_key

            # 防止空值
        if not request_query:
            query_key = "-"

        return query_key

    @staticmethod
    def callback_func(data=None, meta=None) -> tuple[any, any]:
        return data, meta

    # 缓存集合筛选 : apiCache.GetCollect(hKey, "&_page=1")
    def collect(self, hkey: str, query_key: str, callback: callback_func, expire: int = 0) -> tuple[any, any]:
        data, meta = self.get_data_by_mine_key(hkey, query_key)
        print("result, meta::", data, meta)  #
        # 无缓存则添加
        if data is None or self.query.get("_time") == 1:
            print("api-realtime:", hkey + query_key)  #
            # 获取闭包返回内容
            data, meta = callback()
            # 设置db集合全局信息
            self.set_db_info(hkey, expire)
            # 添加缓存
            self.set_data_by_mine_key(hkey, query_key, data, meta, expire)
            # 更新db集合全局信息
            self.update_db_info(hkey)

        return data, meta

    # 获取数据
    def get_data_by_mine_key(self, hkey: str, query_key: str) -> tuple[any, any]:
        data = None
        meta = None
        json_str = self.rdb.hget(hkey, query_key)
        if json_str and len(json_str) > 0:
            json_data = json.loads(json_str)
            if json_data.get("data"):
                data = json_data["data"]
            if json_data.get("meta"):
                meta = json_data["meta"]
        return data, meta

    # 保存数据
    def set_data_by_mine_key(self, hkey: str, query_key: str, data: any, meta: any = None, expire: int = 0) -> None:
        data_dict = {"data": data, "meta": meta}
        # orm结构 转 json字典
        json_data = jsonable_encoder(data_dict)
        # 字典 转 json文本
        json_str = json.dumps(json_data)
        self.rdb.hset(hkey, query_key, json_str)
        # 不过期, 则不设置
        if expire > 0:
            self.rdb.expire(hkey, expire)
        return

    # 设置db集合全局信息
    def set_db_info(self, hkey: str, expire: int = 0) -> None:
        keys_dict = self.rdb.hkeys(hkey)
        if not keys_dict:
            # 哈希键不存在时, 需要先设置过期时间, 作用于所有子键.
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.rdb.hset(hkey, "db_total", "0")
            self.rdb.hset(hkey, "db_expire", str(expire))
            self.rdb.hset(hkey, "db_create_time", now_str)
            self.rdb.hset(hkey, "db_update_time", now_str)
            self.rdb.expire(hkey, expire)
        return

    # 更新db集合全局信息
    def update_db_info(self, hkey: str) -> None:
        keys_dict = self.rdb.hkeys(hkey)
        db_total = len(keys_dict) - 4
        if keys_dict:
            # 哈希键存在时, 子数据添加.
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.rdb.hset(hkey, "db_total", str(db_total))
            self.rdb.hset(hkey, "db_update_time", now_str)
        return

    # 缓存集合清理
    def drop_store(self, hkey: str):
        self.rdb.expire(hkey, -1)
        pass

    # 缓存集合筛选 : api_cache.get_collect(hkey, "&_page=1")
    def get_collect(self, hkey: str, query_key: str):
        pass

    # 缓存集合-部分键清理 : api_cache.drop_collect(hkey, "&_page=1")
    def drop_collect(self, hkey: str, query_key: str):
        pass
