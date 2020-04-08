# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/4 18:40
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :权限相关的类视图
"""
from datetime import timedelta
from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_admin.auth.depends import authenticate_user, create_access_token, get_current_active_user, \
    get_password_hash
from fastapi_admin.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from ..auth.schemas import UserSchema, RegisterUser

from .models import User
from pydantic import EmailStr
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录账户，获取token
    :param form_data:
    :return:
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
async def user_register(form_data:RegisterUser):
    """注册用户"""


# 创建一个User的特殊view


def create_create(model, database):
    async def create(instance: UserSchema = Body(..., ), current_user: User = Depends(get_current_active_user)):
        instance.password = get_password_hash(instance.password)
        query = model.__table__.insert().values(dict(instance))
        return await database.execute(query)

    return create


async def create_superuser(model, database, instance: UserSchema = Body(..., )):
    """创建超级管理员"""
    instance.password = get_password_hash(instance.password)
    query = model.__table__.insert().values(dict(instance))
    return await database.execute(query)


def create_User_View(model, database):
    pass

