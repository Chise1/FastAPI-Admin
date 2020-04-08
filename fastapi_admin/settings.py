# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/4/5 22:22
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

# to get a string like this run:
# openssl rand -hex 32
#秘钥
SECRET_KEY = "1602a122e1e731bf18b47d4494092572c25b8df5c6aa59742f2a985743f695a1"
#加密算法
ALGORITHM = "HS256"
#token过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7