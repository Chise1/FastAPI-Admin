# -*- encoding: utf-8 -*-
"""
@File    : depends.py
@Time    : 2020/4/5 22:19
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :auth的公共依赖项和类似依赖的函数
"""

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.sql import select

from .schemas import UserDB, TokenData
from ..databaseManage import AdminDatabase
from .models import User
# 加密解密用的方法
from ..settings import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 登录依赖
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    """
    密码验证
    :param plain_password: 原始密码
    :param hashed_password:加密的密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str) -> UserDB:
    """
    从数据库通过username获取user
    :param db:
    :param username:
    :return:
    """
    print("需要调试")
    database = AdminDatabase().database
    query = User.__table__.select().where(User.username == username)
    user = await database.fetch_one(query)
    if user:
        return UserDB(**user)


async def authenticate_user(username: str, password: str):
    """
    验证user是否有效
    :param fake_db:数据库
    :param username: 用户名
    :param password: 原始密码
    :return:
    """
    user = await get_user(username)
    # print(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    创建token
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 每操作一次延长十五分钟有效期
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # expire过期时间
    # 加密过期时间和data数据
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    根据token获取user
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 获取解密信息
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    判断是否有效
    :param current_user:
    :return:
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="已禁用")
    return current_user
def get_password_hash(password):
    """
    获取密码的hash值
    :param password:原值密码
    :return:
    """
    return pwd_context.hash(password)