# -*- encoding: utf-8 -*-
"""
@File    : test_selializers.py
@Time    : 2020/4/1 1:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :尝试将model转为basemodel的类，实现操作
"""
from pydantic import BaseModel, Field
from typing import NewType

from sqlalchemy import Integer, Table

UserId = NewType('UserId', int)
admin_basemodel = []
from typing import Any
from fastapi import APIRouter
class RouterBaseModel(BaseModel):
    @staticmethod
    def list(model,db):
        """methods=get，读取列表"""
        def res():
            return db.query(model).all()
            # print(model.__table__.select())
        return res
    def write2route(self,ul,route:APIRouter,model,get_db):
        route.get(ul)(self.list(model,get_db))
    class Config:
        orm_mode = True
def get_basemodel(cls):
    model_name = cls.__name__
    table = cls.__table__
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}

    for filed in cls.__table__.c:
        filed_name = str(filed).split('.')[-1]

        if filed.default:
            default_value = filed.default
        elif filed.nullable:
            default_value = ...
        else:
            default_value = None

        res_field = Field(default_value, description=filed.description)  # Field参数
        if isinstance(filed.type, Integer):
            tp = NewType(filed_name, int)
        else:
            tp = NewType(filed_name, str)

        __mappings__[filed_name] = {'tp': tp, 'Field': res_field}
    res = type(model_name, (RouterBaseModel,), __mappings__)
    cls.__model__=res()
    # admin_basemodel.append(res)
    # print(admin_basemodel)
    return cls
