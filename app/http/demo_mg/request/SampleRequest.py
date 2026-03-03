from typing import Annotated, List, Union, Optional
from pydantic import BaseModel, Field


# 公共验证
class Common(BaseModel):
    # model_config = {"extra": "forbid"}  # 包含/禁止
    id: str = Field(default=None)
    name: str = Field(default=None)
    mobile: str = Field(default=None)
    sex: int = Field(default=None, gt=0)
    type: int = Field(default=None)
    status: int = Field(default=None)
    created_at: str = Field(default=None)
    updated_at: str = Field(default=None)
    deleted_at: str = Field(default=None)


# 验证模型-新增
class Save(Common):
    mobile: str = Field()


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
