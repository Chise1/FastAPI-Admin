# -*- encoding: utf-8 -*-
"""
@File    : method_get.py
@Time    : 2020/4/8 14:29
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :生成get相关的方法
"""
from typing import List, Optional, Callable
from ..auth.models import User
from fastapi import Depends
from pydantic import BaseModel
from .. import page_query, AdminDatabase
from ..auth.depends import create_current_active_user
from ..schema_tools import create_get_page_schema, create_get_schema
__all__=['model_get_list_func','model_get_func_fetch_one']

def model_get_list_func(model, default_model_name=None, exclude: Optional[List[str]] = None,
                        fields: Optional[List[str]] = None,need_login=True) -> (Callable, BaseModel):
    """根据model生成列表get的带列表和分页的数据"""
    if not default_model_name:
        default_model_name=model.__name__+"Get"
    schema = create_get_page_schema(model, default_model_name, exclude, fields)

    return page_query(model,need_login=need_login), schema


def model_get_func_fetch_one(model, default_model_name=None, exclude: Optional[List[str]] = None,
                   fields: Optional[List[str]] = None,res_func_name=None,need_user=True) -> (Callable, BaseModel):
    """根据model生成get"""
    schema = create_get_schema(model, default_model_name, exclude, fields)
    if need_user:
        async def res(current_user: User = Depends(create_current_active_user(need_user))):
            # if fields:
            #     # query=select([ getattr(model,i) for i in fields ])
            #     query= select([getattr(model.__table__.c, i) for i in fields])
            #     # query = model.__table__.select([getattr(model.__table__.c, i) for i in fields])
            # else:
            #     query = model.__table__.select()
            query = model.__table__.select()
            paginate_obj = await AdminDatabase().database.fetch_one(query)
            return paginate_obj
    else:
        async def res():
            # if fields:
            #     # query=select([ getattr(model,i) for i in fields ])
            #     query= select([getattr(model.__table__.c, i) for i in fields])
            #     # query = model.__table__.select([getattr(model.__table__.c, i) for i in fields])
            # else:
            #     query = model.__table__.select()
            query = model.__table__.select()
            paginate_obj = await AdminDatabase().database.fetch_one(query)
            return paginate_obj
    if not res_func_name:
        if not default_model_name:
            model_name = model.__name__
        else:
            model_name = default_model_name
    else:
        model_name=res_func_name
    res.__name__=model_name

    return res, schema
