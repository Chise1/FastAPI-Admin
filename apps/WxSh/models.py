# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/11 11:39
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Column, String, Integer, Boolean, Date, Text
from fastapi_admin.auth.models import Base
class ServiceProviders(Base):
    """服务商列表"""
    __tablename__="wxsh_serviceproviders"
    id=Column(Integer,primary_key=True,comment="服务商编号")
    name=Column(String(32),comment="服务商名称")
    mach_id=Column(String(32),comment="服务商配置machid")
    key=Column(String(32),comment="服务商配置key")
    apiv3_key=Column(String(32),comment="服务商配置aplv3_key")
    wx_appid=Column(String(32),comment="服务商绑定的appid")
    zfb_appid=Column(String(32),comment="支付宝appid")
    afb_appsecret=Column(String(32),comment="支付宝secret")
    certificate=Column(Text,comment="证书")
    private_key=Column(Text,comment="秘钥")
    status=Column(Boolean,comment="状态")
    # type=Column(String(8),comment="服务商类型")#官方，私有，公有


class BusinessManager(Base):
    """商户超级管理员"""
    __tablename__ = "wxsh_businessmanager"
    id = Column(Integer, primary_key=True)
    name=Column(String(32),comment="姓名")
    card_id=Column(String(18),comment="身份证件号码")
    phone_number=Column(String(11),comment="手机号码")
    email=Column(String(32),comment="邮箱")
    #主体资料
    BUSSINESS_TYPE=((0,"个体户"),(1,"企业"))
    business_type=Column(Integer,comment="主体类型"+str(BUSSINESS_TYPE),default=0)
    BUSSINESS_CARD_TYPE=((0,"中国大陆居民-身份证"),)
    business_card_type=Column(Integer,comment="经营者/法人身份证件"+str(BUSSINESS_TYPE))
    bussiness_name=Column(String(32),comment="商户名称")
    business_manager_name=Column(String(32),comment="个体经营者/法人姓名")
    is_favoree=Column(Boolean,comment="经营者/法人是否是受益人")
    register_number=Column(String(32),comment="注册号/统一社会信用代码")
    business_license_photo=Column(String(255),comment="营业执照照片")
    #法人信息
    corporate_name=Column(String(16),comment="法人身份证姓名")
    corporate_card_id=Column(String(18),comment="法人身份证号码")
    corporate_card_start_time=Column(Date,comment="身份证有效期开始时间")
    corporate_card_end_time=Column(Date,comment="身份证有效期结束时间")
    corporate_card_image_front=Column(String(255),comment="身份证国徽面照片")
    corporate_card_image_backend=Column(String(255),comment="身份证人像照")
    #经营资料
    bussiness_name_short=Column(String(18),comment="商户简称")
    service_tel=Column(String(11),comment="客服电话")
    WORKING_GROUP_CHOICE=((0,"线下门店"),(1,"公众号"))
    working_group=Column(Integer,comment="经营场景类型")
    INDUSTRY_INVOLVED=((0,"培训机构"),)
    industry_involved=Column(Integer,comment="所属行业")
    special_certification=Column(String(255),comment="特殊资质")#照片
    # 公众号资料
    gzh_appid=Column(String(64),comment="公众号appid")
    gzh_image=Column(String(255),comment="公众号页面截图")

    #结算银行账户
    ACCOUNT_TYPE=((0,"对公银行账户"),(1,"经营这个人银行卡"))
    account_type=Column(Integer,comment="账户类型")
    account_user_name=Column(String(18),comment="开户人姓名")
    ACCOUNT_BANK=((0,"工商银行"),)
    account_bank=Column(Integer,comment="开户行")
    account_bank_address=Column(String(255),comment="开户行省市")
    account_id=Column(String(32),comment="银行账号")


class Order(Base):
    __tablename__ = "wxsh_order"
    id = Column(Integer, primary_key=True, index=True,comment="订单号")
    bussiness_order_id=Column(String(32),comment="商户订单号")
    offical_order_id = Column(String(32), comment="官方订单号")
    user_id=Column(Integer,comment="商户ID")
    channel_id=Column(String(32),comment="通道id")#对应服务商列表
    goods_name=Column(String(32),comment="商品名称")
    transaction_amount=Column(String(255),comment="交易金额")
    transaction_domain=Column(String(32),comment="交易域名")
    TRANSCATION_TYPE=(('wxpay',"微信"),('alipay',"支付宝"))
    transaction_type=Column(String,comment="交易类型"+str(TRANSCATION_TYPE))#付款类型
    STATUS=((1,"已支付"),(0,"未支付"),(2,"已退款"))
    status=Column(Integer,comment="状态"+str(STATUS),default=0)
    finish_time=Column(DateTime,comment="交易时间/完成时间")
    create_time=Column(DateTime,comment="创建时间",default=datetime.now)
    inform_address=Column(String(255),comment="异步通知地址")
    inform=Column(String(255),comment="异步返回数据")
