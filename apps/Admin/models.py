# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/1 0:30
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from pydantic import  BaseModel
from sqlalchemy.orm import relationship

from apps.Admin.test_selializers import get_basemodel
from databases import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

@get_basemodel
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True,default="chise123@live.com")
    hashed_password = Column(String(64))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

@get_basemodel
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    description = Column(String(64), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")