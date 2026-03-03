from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# 模型父类
class BaseEntity(DeclarativeBase):
    pass
