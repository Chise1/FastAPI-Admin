# -*- encoding: utf-8 -*-
"""
@File    : methods_post.py
@Time    : 2020/4/11 18:44
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional, List, Callable

from fastapi import Depends
from pydantic import BaseModel

from fastapi_admin import User, AdminDatabase
from fastapi_admin.auth.depends import create_current_active_user
from fastapi_admin.schema_tools import create_get_schema


def model_post_func(model, default_model_name=None, exclude: Optional[List[str]] = None,
                    fields: Optional[List[str]] = None, res_func_name=None, need_user=True) -> (
        Callable, BaseModel):
    """根据model生成post创建接口"""
    res_schema=create_get_schema(model, default_model_name, exclude, fields)
    if not exclude and not fields:
        exclude = ['id']
    elif exclude:
        exclude.append('id')
    schema = create_get_schema(model, default_model_name, exclude, fields)

    async def res(post_dict: schema, current_user: User = Depends(create_current_active_user(need_user))):
        res_dict = dict(post_dict)
        query = model.__table__.insert().values(res_dict)
        res_dict.update({"id": await AdminDatabase().database.execute(query)})
        return res_dict

    if not res_func_name:
        if not default_model_name:
            model_name = model.__name__
        else:
            model_name = default_model_name
    else:
        model_name = res_func_name
    res.__name__ = model_name
    return res, res_schema
