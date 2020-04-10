# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/10 13:43
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from decimal import Decimal
from typing import List

from pydantic import BaseModel, DecimalError, Field

from fastapi_admin import User
from fastapi_admin.publicDepends.paging_query import PagingModel


class UserModel(BaseModel):
    id:int=None
    obj_guid:str=None
    username:str=None
    email:str=None
    qq:str=None
    money:Decimal=None
    rate:Decimal=None
    is_active:bool=None
class UserListModel(PagingModel):
    data:List[UserModel]=[]

from fastapi_admin.schema_tools import create_get_schema
UpdateUserInfo=create_get_schema(User,default_model_name="UpdateUserInfo",fields=['id','nick_name','email','qq'])
