# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2020/4/14 14:54
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :一些工具
"""
from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext
from pymysql import IntegrityError
from starlette import status

from ..settings import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    获取密码的hash值
    :param password:原值密码
    :return:
    """
    return pwd_context.hash(password)


def get_exception_info(e: IntegrityError):
    """mysql报错处理"""
    # if e.args[0] == 1048:#字段不能为空
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=e.args[1],
    #         # headers={"WWW-Authenticate": "Bearer"},
    #     )
    # else:
    #     pass
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=e.args[1],
        # headers={"WWW-Authenticate": "Bearer"},
    )