# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/11 14:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from datetime import datetime
from enum import Enum,IntEnum
from pydantic import BaseModel, Field,AnyHttpUrl,Json

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
    status:OrderStatusEnum=Field(OrderStatusEnum.unpaid,description="订单状态")

class OrderPostSchema(BaseModel):
    platform_id:str = Field(..., comment="平台订单号")
    bussiness_order_id:str = Field(..., comment="商户订单号")
    offical_order_id:str = Field(..., comment="官方订单号")
    user_id:int = Field(..., comment="商户ID")
    channel_id:str = Field(..., comment="通道id")  # 对应服务商列表
    goods_name:str = Field(..., comment="商品名称")
    transaction_amount:str = Field(..., comment="交易金额")
    transaction_domain :str= Field(..., comment="交易域名")
    transaction_type:TransactionType = Field(TransactionType.jsapi, comment="交易类型")  # 付款类型
    status:OrderStatusEnum = Field(OrderStatusEnum.unpaid, comment="状态")
    finish_time:datetime = Field(None, comment="交易时间/完成时间")
    create_time:datetime = Field(datetime.now(), comment="创建时间", )
    inform_address:AnyHttpUrl = Field(..., comment="异步通知地址")
    inform:Json = Field(None, comment="异步返回数据")

class OrderPostRes(OrderPostSchema):
    id:int
    class Config:
        orm_mode = True
