# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/7 20:36
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from sqlalchemy import Column, String,Integer,Float

from ..databaseManage import Base


class Config(Base,):
    """fastapi_config_config"""
    __tablename__="fastapi_config_config"
    id = Column(Integer, primary_key=True, index=True)
    web_name=Column(String(64),comment="网站标题",nullable=False)
    subTitle=Column(String(64),comment="副标题")
    seoIntroduce=Column(String(128),comment="seo介绍")
    seoKwargs=Column(String(128),comment="seo关键词")
    serve_qq=Column(String(16),comment="客服qq")
    currency=Column(String,comment="币种",default="RNY")
    ratio=Column(Float,comment="兑换⽐例；（1⼈名币等于多少积分")
    smtp_host=Column(String(32),comment="邮箱ip",nullable=True)
    smtp_port=Column(Integer,comment="邮箱port",nullable=True)
    smtp_email=Column(String(32),comment="邮箱地址",nullable=True)
    smtp_email_password = Column(String(32), comment="邮箱地址", nullable=True)
    visitor_address=Column(String(128),comment="游客登录地址",nullable=True)
    user_default_lv=Column(Integer,comment="用户默认等级",default=0)
    manager_email=Column(String(32),comment="默认邮箱")