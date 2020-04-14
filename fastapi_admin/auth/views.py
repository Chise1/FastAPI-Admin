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
from pymysql import IntegrityError
from sqlalchemy import insert

from apps.AdminManager.models import AccountBook
from fastapi_admin.auth.depends import authenticate_user, create_access_token, get_current_active_user, \
    get_password_hash, create_current_active_user
from fastapi_admin.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .models import User
from .tools import get_exception_info
from ..schema_tool import create_schema
from ..databaseManage import AdminDatabase
from ..auth.schemas import UserSchema, RegisterUser
from  fastapi import APIRouter
router=APIRouter()
#测试tortoise.models



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



@router.post('/v1/user/register',name="普通用户注册",description="普通用户的注册功能")
async def user_register(form_data: RegisterUser):
    """注册用户"""
    # print(form_data)
    default_info={
        "is_superuser":False,
        "is_active":True
    }
    register_info=dict(form_data)
    register_info['password']=get_password_hash(form_data.password)
    default_info.update(register_info)
    db=AdminDatabase().database
    if not default_info.get('guid'):
        default_info['guid'] = "1" + createGuid(4)
    query = User.__table__.insert().values(default_info)
    try:
        default_info['id']=await db.execute(query)
        default_info.pop('password')
        schema=create_schema(AccountBook,"AccountBookCreate",exclude=['id'])
        schema_value=schema(**{"user_id":default_info['id']})
        schema_value.member_id=1
        await db.execute( insert(AccountBook).values(dict(schema_value)))

        return default_info
    except IntegrityError as e:
        get_exception_info(e)
    except Exception as e:
        print(e)
        raise Exception("服务器内部错误")
    return {"code":200,"msg":"success"}


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
        if not instance.guid:
            instance.guid = "1" + createGuid(4)
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
