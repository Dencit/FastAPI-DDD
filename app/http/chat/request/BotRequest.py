from typing import Annotated, List, Union, Optional
from pydantic import BaseModel, Field


# 公共验证
class Common(BaseModel):
    role: str = Field()
    content: str = Field()


# 验证模型-新增
class Save(Common):
    pass


# 验证模型-更新
class Update(Common):
    pass


# 验证模型-删除
class Delete(Common):
    pass


# 验证模型-获取行
class Read(Common):
    pass


# 验证模型-获取列表
class Index(Common):
    pass
