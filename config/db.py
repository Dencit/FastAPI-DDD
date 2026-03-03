from functools import lru_cache
from pydantic_settings import BaseSettings


# 配置类
@lru_cache
class DbSettings(BaseSettings):
    # 打印sql
    debug: bool = False
    # redis server
    redis: dict = {
        "host": '127.0.0.1',
        "port": '6379',
        "username": "root",
        "password": "root",
        "db": '0',
    }
    # demo_mg 数据库
    mongo: dict = {
        'default': {
            'ENGINE': 'mongodb',
            'NAME': 'admin',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': '127.0.0.1',
            'PORT': "27017",
        }
    }
    # mysql 数据库
    databases: dict = {
        'default': {
            'ENGINE': 'mysql+pymysql',
            'NAME': 'fastapi_db',  # 你的数据库名称 数据库需要自己提前建好
            'USER': 'root',  # 你的数据库用户名
            'PASSWORD': 'root',  # 你的数据库密码
            'HOST': 'localhost',  # 你的数据库主机，留空默认为localhost
            'PORT': '3306',  # 你的数据库端口
            'OPTIONS': {}
        }
    }
