from functools import lru_cache
from redis import ConnectionPool, Redis
from config.db import DbSettings


class Rdb(object):
    conn: Redis = None

    @lru_cache
    def client(self, select: int = 0):
        if self.conn is None:
            db = 0
            if select > 0:
                db = select

            conf = DbSettings().redis
            confs = {
                "host": conf["host"],
                "port": conf["port"],
                "username": conf["username"],
                "password": conf["password"],
                "db": db,
            }
            pool = ConnectionPool(**confs)
            self.conn = Redis(connection_pool=pool)
        return self.conn
