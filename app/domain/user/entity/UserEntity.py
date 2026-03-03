from datetime import datetime
from sqlalchemy import String, Text, BigInteger, SmallInteger, DateTime, Numeric
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column
#
from app.base.entity.entity import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(255), default="")
    name: Mapped[str] = mapped_column(String(255), default="")
    nick_name: Mapped[str] = mapped_column(String(255), default="")
    avatar: Mapped[str] = mapped_column(String(255), default="")
    sex: Mapped[int] = mapped_column(SmallInteger(), default=0)
    mobile: Mapped[str] = mapped_column(String(30), default="")
    pass_word: Mapped[str] = mapped_column(String(255), default="")
    client_driver: Mapped[str] = mapped_column(Text(), default="")
    client_type: Mapped[int] = mapped_column(SmallInteger(), default=0)
    lat: Mapped[float] = mapped_column(Numeric(10, 6), default=0.0)
    lng: Mapped[float] = mapped_column(Numeric(10, 6), default=0.0)
    status: Mapped[int] = mapped_column(SmallInteger(), default=0)
    on_line_time: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
    off_line_time: Mapped[datetime] = mapped_column(DateTime(), default=None)
    created_at: Mapped[str] = mapped_column(DateTime(), nullable=False, insert_default=datetime.now)
    updated_at: Mapped[str] = mapped_column(DateTime(), nullable=False, insert_default=datetime.now, default=datetime.now)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(), default=None)

    # 定义Config属性，用于配置
    class Config:
        # 设置from_orm属性，值为True
        from_orm = True
        populate_by_name = True


@event.listens_for(User, 'before_insert')
def before_insert(mapper, connection, target):
    print("BEFORE_INSERT::", target)


@event.listens_for(User, 'after_insert')
def after_insert(mapper, connection, target):
    print("AFTER_INSERT::", target)


@event.listens_for(User, 'after_update')
def after_update(mapper, connection, target):
    print("AFTER_UPDATE::", target)


@event.listens_for(User, 'before_update')
def after_update(mapper, connection, target):
    print("BEFORE_UPDATE::", target)


@event.listens_for(User, 'before_delete')
def before_delete(mapper, connection, target):
    print("BEFORE_DELETE::", target)


@event.listens_for(User, 'after_delete')
def after_delete(mapper, connection, target):
    print("AFTER_DELETE::", target)
