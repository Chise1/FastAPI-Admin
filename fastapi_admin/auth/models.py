# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/4 15:31
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :创建基本需要的models
"""
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table

__all__=['User','Group','Permission']
Base = declarative_base()

class User(Base):
    __tablename__ = 'fastapi_auth_user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    password = Column(String(128), )
    is_superuser = Column(Boolean, default=False)
    email = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=True)
    def __str__(self):
        return self.username

auth_user_group = Table(  # 多对多的第三方表，居然还要自己生成。。
    'fastapi_auth_user_group',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("fastapi_auth_user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("fastapi_auth_group.id"), primary_key=True)
)


class Group(Base):
    __tablename__ = 'fastapi_auth_group'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, index=True)
    users = relationship("User", backref="groups", secondary=auth_user_group)
    def __str__(self):
        return self.name

auth_group_permission = Table(  # 多对多的第三方表，居然还要自己生成。。
    'fastapi_auth_group_permission',
    Base.metadata,
    Column("group_id", Integer, ForeignKey("fastapi_auth_group.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("fastapi_auth_permission.id"), primary_key=True)
)


class Permission(Base):
    __tablename__ = 'fastapi_auth_permission'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True)  # 权限名称
    codename = Column(String(100), unique=True, index=True)  # 权限字段
    groups = relationship("Group", backref="permissions", secondary=auth_group_permission)
    def __str__(self):
        return self.name
