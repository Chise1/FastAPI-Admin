# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2020/4/5 20:35
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from passlib.context import CryptContext
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "1602a122e1e731bf18b47d4494092572c25b8df5c6aa59742f2a985743f695a1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password,hashed_password):
    """"""
    return pwd_context.verify(plain_password,hashed_password)