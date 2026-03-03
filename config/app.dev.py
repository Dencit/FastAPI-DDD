from functools import lru_cache
from pydantic_settings import BaseSettings


# 配置类
@lru_cache
class AppSettings(BaseSettings):
    # 不要在生产中打开调试的情况下运行
    debug: bool = False
    # 百度智能云
    qianfan: dict = {
        "access_key": "xxx",
        "secret_key": "xxx",
        "api_key": "xxxx",
        "base_host": "https://qianfan.baidubce.com/v2/chat/completions"
    }
    # 百度智能云-大模型ID
    models: dict = {
        "bge-large-en": "svcp-d759175d1277",  # 英文向量模型
        "bge-large-zh": "svcp-fb60d4111276",  # 中文向量模型
        "tao-8k": "svcp-e56b06c51373",  # 中文长文本向量模型
        "embedding-v1": "svcp-6c14da101231",  # 文本向量模型
        "bce-reranker-base": "svcp-0a1bf96b1455",  # 语义搜索排序模型
        "deepseek-r1": "svcp-6a508a601951",
        "deepseek-v3": "svcp-a38b16171953",
    }
