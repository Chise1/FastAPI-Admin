# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/7 20:36
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from ..schema_tools import create_schema,__create_one_schema
from .models import Config
BaseConfig=__create_one_schema(Config,default_model_name="BaseConfig",fields=["web_name","subTitle","seoIntroduce","seoKwargs","serve_qq","currency","ratio","user_default_lv","manager_email"])

EmailConfig=__create_one_schema(Config,default_model_name="EmailConfig",fields=["smtp_host","smtp_port","smtp_email","smtp_email_password"])
