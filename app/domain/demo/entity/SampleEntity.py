from datetime import datetime
from typing import Set
from sqlalchemy import String, BigInteger, SmallInteger, DateTime, ForeignKey
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column, relationship
#
from app.base.entity.entity import BaseEntity
from app.domain.user.entity import UserEntity


class Sample(BaseEntity):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(BigInteger(), ForeignKey(UserEntity.User.id), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), default="")
    mobile: Mapped[str] = mapped_column(String(30), default="")
    photo: Mapped[str] = mapped_column(String(200), default="")
    sex: Mapped[int] = mapped_column(SmallInteger(), default=0)
    type: Mapped[int] = mapped_column(SmallInteger(), default=0)
    status: Mapped[int] = mapped_column(SmallInteger(), default=0)
    created_at: Mapped[str] = mapped_column(DateTime(), nullable=False, insert_default=datetime.now)
    updated_at: Mapped[str] = mapped_column(DateTime(), nullable=False, insert_default=datetime.now)
    deleted_at: Mapped[str] = mapped_column(DateTime(), default=None)

    user: Mapped[dict] = relationship(UserEntity.User, overlaps="user")
    users: Mapped[Set[dict]] = relationship(UserEntity.User, overlaps="user", uselist=True)

    # 只要 未软删除

    def with_trashed(self):
        return self.query().filter(deleted_at=None)

    # 定义Config属性，用于配置
    class Config:
        # 设置from_orm属性，值为True
        from_orm = True
        populate_by_name = True


@event.listens_for(Sample, 'before_insert')
def before_insert(mapper, connection, target):
    print("BEFORE_INSERT::", target)


@event.listens_for(Sample, 'after_insert')
def after_insert(mapper, connection, target):
    print("AFTER_INSERT::", target)


@event.listens_for(Sample, 'after_update')
def after_update(mapper, connection, target):
    print("AFTER_UPDATE::", target)


@event.listens_for(Sample, 'before_update')
def after_update(mapper, connection, target):
    print("BEFORE_UPDATE::", target)


@event.listens_for(Sample, 'before_delete')
def before_delete(mapper, connection, target):
    print("BEFORE_DELETE::", target)


@event.listens_for(Sample, 'after_delete')
def after_delete(mapper, connection, target):
    print("AFTER_DELETE::", target)
