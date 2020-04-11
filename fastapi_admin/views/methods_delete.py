# -*- encoding: utf-8 -*-
"""
@File    : methods_delete.py
@Time    : 2020/4/11 16:56
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Callable

from fastapi import Depends
from pydantic import BaseModel

from fastapi_admin import User, AdminDatabase
from fastapi_admin.auth.depends import create_current_active_user

def model_delete_func(model, default_model_name=None, res_func_name=None,need_user=True) -> (Callable, BaseModel):
    """根据model生成删除"""
    async def res(id,current_user: User = Depends(create_current_active_user(need_user))):
        query = model.__table__.delete().where(model.id==id)
        await AdminDatabase().database.fetch_one(query)
        return query
    if not res_func_name:
        if not default_model_name:
            model_name = model.__name__
        else:
            model_name = default_model_name
    else:
        model_name=res_func_name
    res.__name__=model_name
    return res