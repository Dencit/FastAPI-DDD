from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
#
from config.db import DbSettings

"""doc - https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker"""


class Db:
    engine: create_engine = None

    def get_engine(self):
        if self.engine is None:
            # 读取数据库配置
            settings = DbSettings()
            # 引用值
            is_debug = settings.debug
            default = settings.databases["default"]
            engine = default['ENGINE'] if len(default['ENGINE']) > 0 else ""
            user = default['USER'] if len(default['USER']) > 0 else ""
            pass_word = default['PASSWORD'] if len(default['PASSWORD']) > 0 else ""
            host = default['HOST'] if len(default['HOST']) > 0 else "localhost"
            port = default['PORT'] if len(default['PORT']) > 0 else '3306'
            db_name = default['NAME'] if len(default['NAME']) > 0 else ""
            db_host = f"{engine}://{user}:{pass_word}@{host}:{port}/{db_name}"
            pool_size = 10
            max_overflow = 20
            pool_recycle = -1
            self.engine = create_engine(
                db_host,
                echo=is_debug,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_recycle=pool_recycle
            )
        return self.engine

    @contextmanager
    def contextmanager(self, auto_commit_by_exit=True):
        engine = self.get_engine()
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        try:
            yield session
            # 退出时，是否自动提交
            if auto_commit_by_exit:
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_session(self):
        with self.contextmanager() as session:
            return session
