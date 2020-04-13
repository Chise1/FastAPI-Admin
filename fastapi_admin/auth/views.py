# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/4 18:40
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :权限相关的类视图
"""
import random
from datetime import timedelta
from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_admin.auth.depends import authenticate_user, create_access_token, get_current_active_user, \
    get_password_hash, create_current_active_user
from fastapi_admin.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .models import User
from ..auth.schemas import UserSchema, RegisterUser


async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录账户，获取token
    :param form_data:
    :return:
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def user_register(form_data: RegisterUser):
    """注册用户"""
    pass


# 创建一个User的特殊view
def createGuid(num: int)->str:
    guid = ''
    for i in range(1, num):
        start = 0 if (i % 2) == 0 else 1
        rand = random.randint(start, 9)
        guid = guid + str(rand)
    return guid


def create_create(model, database):
    async def create(instance: RegisterUser = Body(..., ),
                     current_user: User = Depends(create_current_active_user(True))):
        print("instance:", instance)
        if not instance.obj_guid:
            instance.obj_guid = "1" + createGuid(4)
        instance.password = get_password_hash(instance.password)
        query = model.__table__.insert().values(dict(instance))
        try:
            instance.id= await database.execute(query)
            return instance
        except Exception as e:
            print("注意根据不同数据库返回不同异常")
            raise HTTPException(status_code=400, detail=str(e))
    return create


async def create_superuser(model, database, instance: UserSchema = Body(..., )):
    """创建超级管理员"""
    instance.password = get_password_hash(instance.password)
    query = model.__table__.insert().values(dict(instance))
    return await database.execute(query)


def create_User_View(model, database):
    pass
# async def get_user
#
# async def delete_user(model,)