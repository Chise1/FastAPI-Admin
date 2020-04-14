# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/11 14:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import math
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, func, insert

from fastapi_admin import User, AdminDatabase
from fastapi_admin.auth.depends import create_current_active_user
from fastapi_admin.publicDepends.paging_query import paging_query_depend
from .schemas import TransactionType, OrderStatusEnum, OrderPostSchema, OrderPostRes

router = APIRouter()
from .models import Order
from fastapi_admin.views.methods_get import model_get_list_func
from fastapi_admin.views.methods_post import model_post_func

order_get_list, schema = model_get_list_func(Order, )
order_post, order_post_schema = model_post_func(Order)
router.post('/order', name="创建订单", deprecated=True, response_model=order_post_schema)(order_post)


@router.post('/v2/order', name='创建订单', deprecated=True, response_model=OrderPostRes)
async def order_post(order_info: OrderPostSchema, current_user: User = Depends(create_current_active_user(True))):
    print(order_info)
    res = dict(order_info)
    query = insert(Order).values(res)
    res['id'] = await AdminDatabase().database.execute(query)
    return res


@router.get('/order', name="订单列表过滤功能测试")
async def order_list(platform: str = Query(None, description="平台订单号"),
                     tenant: str = Query(None, description="商户订单号"),
                     official: str = Query(None, description="官方订单号"),
                     channel_id: str = Query(None, description="通道id"),
                     goods_name: str = Query(None, description="商品名称"),
                     transaction_type: TransactionType = Query(None, description="支付方式"),
                     start_create_time: datetime = Query(None, description="开始时间"),
                     end_create_time: datetime = Query(None, description="截止时间"),
                     status: OrderStatusEnum = Query(None, description="订单状态"),
                     page: Dict[str, int] = Depends(paging_query_depend),
                     current_user: User = Depends(create_current_active_user(True))):
    table = Order.__table__
    query = Order.__table__.select()
    if platform != None:  # 平台订单号
        query = query.where(table.c.platform_id.like('%' + platform + '%'))
    elif tenant != None:
        query = query.where(table.c.bussiness_order_id.like('%' + tenant + '%'))
    elif official != None:
        query = query.where(table.c.offical_order_id.like('%' + official + '%'))
    else:
        if channel_id:
            query = query.where(table.c.channel_id.like('%' + channel_id + '%'))
        if goods_name:
            query = query.where(table.c.goods_name.like('%' + goods_name + '%'))
        if transaction_type:
            query = query.where(table.c.transaction_type == transaction_type)
        if status:
            query = query.where(table.c.status == status)
        if start_create_time:
            query = query.where(table.c.create_time >= start_create_time)
        if end_create_time:
            query = query.where(table.c.create_time <= end_create_time)
        query = query.offset((page['page_number'] - 1) * page['page_size']).limit(
            page['page_size'])  # 第一页，每页20条数据。 默认第一页。

    paginate_obj = await AdminDatabase().database.fetch_all(query)
    query2 = select([func.count(table.c.id)])
    total_page = await AdminDatabase().database.fetch_val(query2)
    res_obj = {
        "page_count": int(math.ceil(total_page * 1.0 / page['page_size'])),
        "rows_total": total_page,
        "page_number": page['page_number'],
        "page_size": page['page_size'],
        "data": paginate_obj
    }
    return res_obj
