from functools import lru_cache
from config.db import DbSettings
from pymongo import MongoClient


class Mdb(object):
    conn: MongoClient = None

    # 获取连接
    @lru_cache
    def client(self):
        if self.conn is None:
            # 读取数据库配置
            settings = DbSettings()
            # 引用值
            default = settings.mongo["default"]
            engine = default['ENGINE'] if len(default['ENGINE']) > 0 else ""
            user = default['USER'] if len(default['USER']) > 0 else ""
            pass_word = default['PASSWORD'] if len(default['PASSWORD']) > 0 else ""
            host = default['HOST'] if len(default['HOST']) > 0 else "localhost"
            port = default['PORT'] if len(default['PORT']) > 0 else "27017"
            mdb_name = default['NAME'] if len(default['NAME']) > 0 else ""
            mdb_host = f"{engine}://{user}:{pass_word}@{host}:{port}/?retryWrites=true&w=majority"
            print("mdb_host::", mdb_host)
            self.conn = MongoClient(mdb_host)
        return self.conn

    # 获取连接 -> 数据集
    def collect(self, db_name, collect_name):
        conn = self.client()
        db = conn[db_name]
        collect = db[collect_name]
        return collect
