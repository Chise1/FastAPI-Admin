# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/11 14:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from enum import Enum,IntEnum
from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    jsapi = 'jsapi'
    native = 'native'
    alipay='支付宝当面付'
    syt='收银台'
class OrderStatusEnum(IntEnum):
    paid=1
    unpaid=0
    refund=2

class OrderFilterSchema(BaseModel):
    id: int = Field(None, description="订单号")
    channel_id :str=Field(None,description="通道id")
    goods_name:str=Field(None,description="商品名称")
    transaction_type:TransactionType=Field(TransactionType.jsapi,description="支付方式")
    status:OrderStatusEnum=Field(OrderStatusEnum.未支付,description="订单状态")
