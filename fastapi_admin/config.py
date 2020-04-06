# -*- encoding: utf-8 -*-
"""
@File    : config.py
@Time    : 2020/4/6 19:49
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :网络配置
"""
from sqlalchemy import Column, String,Integer,Float
from .databaseManage import Base
class Config(Base,):
    web_name=Column(String(64),comment="网站标题",)
    subTitle=Column(String(64),comment="副标题")
    seoIntroduce=Column(String(128),comment="seo介绍")
    seoKwargs=Column(String(128),comment="seo关键词")
    currency=Column(Integer,comment="币种：0人民币，1积分")
    ratio=Column(Float,comment="兑换⽐例；（1⼈名币等于多少积分")
    smtp_host=Column(String(32),comment="邮箱ip",nullable=True)
    smtp_port=Column(Integer,comment="邮箱port",nullable=True)
    smtp_email=Column(String(32),comment="邮箱地址",nullable=True)
    visitor_address=Column(String(128),comment="游客登录地址",nullable=True)
