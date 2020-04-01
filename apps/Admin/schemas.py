# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/1 0:45
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :存储模型的位置
"""
from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True