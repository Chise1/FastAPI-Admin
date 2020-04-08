# -*- encoding: utf-8 -*-
"""
@File    : paging_query.py
@Time    : 2020/4/6 23:58
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :分页依赖
"""
import math
from typing import Dict, List, Optional
from fastapi import Depends
from sqlalchemy import select, func
from fastapi_admin import AdminDatabase

default_page_size = 20


async def paging_query_depend(page_number: int = 1, page_size: int = default_page_size) -> Dict[str, int]:
    """分页依赖"""
    return {"page_number": page_number, "page_size": page_size}


from pydantic import BaseModel, Field


class PagingModel(BaseModel):
    page_count: int
    rows_total: int
    page_number: int
    page_size: int


def get_res_schema(schema, defalut=None):
    """
    生成分页需要的schema
    :param schema:
    :param defalut:
    :return:
    """

    class PagingModel(BaseModel):
        page_count: int
        rows_total: int
        page_number: int
        page_size: int

    class ResModel(PagingModel):
        data: List[schema] = Field(defalut, )

    return ResModel


def page_query(model,):
    """
    分页显示生成器
    :param model:
    :return:
    """

    async def res(page: Dict[str, int] = Depends(paging_query_depend)):
        query = model.__table__.select().offset((page['page_number'] - 1) * page['page_size']).limit(
            page['page_size'])  # 第一页，每页20条数据。 默认第一页。
        paginate_obj = await AdminDatabase().database.fetch_all(query)
        query2 = select([func.count(model.__table__.c.id)])
        total_page = await AdminDatabase().database.fetch_val(query2)
        return {
            "page_count": int(math.ceil(total_page * 1.0 / page['page_size'])),
            "rows_total": total_page,
            "page_number": page['page_number'],
            "page_size": page['page_size'],
            "data": paginate_obj
        }

    return res