# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/4 18:38
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi.security import OAuth2PasswordBearer
#登录要求依赖
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
