# -*- encoding: utf-8 -*-
"""
@File    : methods_patch.py
@Time    : 2020/4/10 15:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :数据局部更新的方法
"""
from typing import Optional,List,Callable

from fastapi import Depends
from pydantic import BaseModel

from fastapi_admin import User, AdminDatabase
from fastapi_admin.auth.depends import create_current_active_user
from fastapi_admin.schema_tools import create_get_schema


def model_patch_func(model, default_model_name=None, exclude: Optional[List[str]] = None,
                                     fields: Optional[List[str]] = None, res_func_name=None, need_user=True) -> (
        Callable, BaseModel):
    """根据model生成get"""
    schema = create_get_schema(model, default_model_name, exclude, fields)
    async def res(id,update_dict:schema,current_user: User = Depends(create_current_active_user(need_user))):
        # if fields:
        #     # query=select([ getattr(model,i) for i in fields ])
        #     query= select([getattr(model.__table__.c, i) for i in fields])
        #     # query = model.__table__.select([getattr(model.__table__.c, i) for i in fields])
        # else:
        #     query = model.__table__.select()
        query = model.__table__.update().values(dict(update_dict)).where(model.id==id)
        print(query)
        await AdminDatabase().database.execute(query)
        return update_dict

    if not res_func_name:
        if not default_model_name:
            model_name = model.__name__
        else:
            model_name = default_model_name
    else:
        model_name = res_func_name
    res.__name__ = model_name

    return res, schema
