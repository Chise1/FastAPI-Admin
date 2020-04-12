# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/11 14:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter
router=APIRouter()
from .models import Order
from fastapi_admin.views.methods_get import model_get_list_func
from fastapi_admin.views.methods_post import model_post_func
order_get_list,schema=model_get_list_func(Order,)
order_post,order_post_schema=model_post_func(Order)
router.get('/order',name="订单列表",description="订单列表",response_model=schema)(order_get_list)
router.post('/order',name="创建订单",response_model=order_post_schema)(order_post)
