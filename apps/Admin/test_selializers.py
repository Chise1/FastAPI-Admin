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

from sqlalchemy import Integer

UserId = NewType('UserId', int)
# admin_basemodel = []
from fastapi import APIRouter


class RouterBaseModel(BaseModel):
    """这个类主要是给生成的schema增加操作"""

    @staticmethod
    def list(model, db):  # 对应get方法
        """methods=get，读取列表"""

        def res():
            return db.query(model).all()
            # print(model.__table__.select())

        return res

    def write2route(self, ul, route: APIRouter, model, get_db):
        """注册到路由"""
        route.get(ul)(self.list(model, get_db))

    class Config:
        orm_mode = True


def get_basemodel(cls):
    """通过读取model的信息，创建schema"""
    model_name = cls.__name__
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}

    for filed in cls.__table__.c:
        filed_name = str(filed).split('.')[-1]

        if filed.default:
            default_value = filed.default
        elif filed.nullable:
            default_value = '...'
        else:
            default_value = 'None'
        # 生成的结构： id:int=Field(...,)大概这样的结构
        # res_field = Field(default_value, description=filed.description)  # Field参数
        res_field = 'Field({}, description={})'.format(default_value,filed.description)  # Field参数

        if isinstance(filed.type, Integer):
            tp = filed_name+':int='
        else:
            tp = filed_name+ 'str='
        __mappings__[filed_name] = {'tp': tp, 'Field': res_field}
    res = type(model_name, (RouterBaseModel,), __mappings__)
    # 将schema绑定到model
    cls.__model__ = res()
    return cls
