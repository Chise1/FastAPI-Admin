# -*- encoding: utf-8 -*-
"""
@File    : schema_factory.py
@Time    : 2020/4/1 22:05
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :将model生成为schema
"""
from typing import NewType
from typing import List
from pydantic import BaseModel, Field
from sqlalchemy import Integer,String
def get_schema(model)->BaseModel:
    s="""
class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass
class View():#测试继承会不会影响basemodel
    def test_view(self):
        print("测试继承")

class Item(ItemBase,View):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
    def test(self):
        return self.title
"""
    mapping={"BaseModel":BaseModel}
    exec (s,mapping)
    # s=Item({"id":1,"owner_id":2})
    return mapping['Item']


def create_schema(model) -> type:
    """
    通过sqlalchemy的model生成pydantic的basemodel
    :param mode:
    :return:
    """
    model_name = model.__name__
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}

    for filed in model.__table__.c:
        filed_name = str(filed).split('.')[-1]
        if filed.default:
            default_value = filed.default
        elif filed.nullable:
            default_value = '...'
        else:
            default_value = 'None'
        # 生成的结构： id:int=Field(...,)大概这样的结构
        res_field = 'Field({}, description={})'.format(default_value, filed.description)  # Field参数
        if isinstance(filed.type, Integer):
            tp = NewType(filed_name, int)
        elif isinstance(filed.type,String):
            tp = NewType(filed_name, str)
        else:
            tp = NewType(filed_name, str)
        __mappings__[filed_name] = {'tp': tp, 'Field': res_field}
    res= type(model_name, (BaseModel,), __mappings__)
    # 将schema绑定到model
    class ResClass(res):
        pass
    return ResClass