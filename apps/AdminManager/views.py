# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/10 13:38
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :后台管理使用的view
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from fastapi_admin import AdminDatabase
from fastapi_admin.auth.schemas import ModifyPassword, ModifyBaseInfo, ForbbidenAccount, DeleteAccount
from fastapi_admin.publicDepends.paging_query import page_base_query
from fastapi_admin.views.methods_patch import model_patch_func
from .models import AccountBook
from .schemas import UserListModel, UserRetrieveModel
from fastapi_admin.auth.depends import create_current_active_user, get_current_active_user, get_password_hash
from fastapi_admin.auth.models import User

router = APIRouter()
# 展示数据
user_list = page_base_query(model=User, default_query=select([User, AccountBook.money, AccountBook.rate]).where(
    AccountBook.user_id == User.id).where(User.is_delete == False), need_user=True)
# 修改数据
user_update, update_schema = model_patch_func(User, "UserUpdateInfo", fields=['nick_name', 'qq', 'email'])


# 修改密码
# user_modify_password,modify_password_schema=model_patch_func(User,"UserModifyPassword",fields=['password'])

async def modify_password(new_password: ModifyPassword, current_user: User = Depends(create_current_active_user(True))):
    """
    修改密码
    :param current_user:
    :return:
    """
    hash_password = get_password_hash(new_password.new_password)
    query = User.__table__.update().values({"password": hash_password}).where(User.id == new_password.id)
    res = await AdminDatabase().database.execute(query)
    return {"code": 200, "message": "success"}


async def modify_base_info(new_info: ModifyBaseInfo, current_user: User = Depends(create_current_active_user(True))):
    """
    修改基础信息
    :param current_user:
    :return:
    """
    query = User.__table__.update().values(dict(new_info)).where(User.id == new_info.id)
    await AdminDatabase().database.execute(query)
    return new_info


async def forbbiden_account(user_id: ForbbidenAccount, current_user: User = Depends(create_current_active_user(True))):
    """
    禁用账户
    :param current_user:
    :return:
    """
    query = User.__table__.update().values({"is_active": user_id.is_active}).where(User.id == user_id.id)
    await AdminDatabase().database.execute(query)
    return user_id


async def delete_account(user_id: DeleteAccount, current_user: User = Depends(create_current_active_user(True))):
    """
    禁用账户
    :param current_user:
    :return:
    """
    query = User.__table__.update().values({"is_delete": True}).where(User.id == user_id.id)
    await AdminDatabase().database.execute(query)
    return user_id


async def user_retrieve(id, current_user: User = Depends(create_current_active_user(True))):
    """获取用户的详细信息"""
    query = select([User,  AccountBook.money,AccountBook.rate]).where(User.id == id).where(AccountBook.user_id == User.id)
    print(query)
    return await AdminDatabase().database.fetch_one(query)
router.get('/admin/user/{id}', tags=['user'],description="查看某个用户的详细信息",summary="查看详情")(user_retrieve)
# router.get('/user/list', tags=['user'], response_model=UserListModel, summary="获取用户列表")(user_list)
router.get('/admin/user', tags=['user'], response_model=UserListModel, summary="获取用户列表")(user_list)

# router.get('/user/list/{id}', tags=['user'], response_model=UserListModel, summary="获取用户列表")(user_list)
router.patch('/user/updateInfo', tags=['user'], response_model=ModifyBaseInfo, summary="更新个人数据")(modify_base_info)
router.patch('/user/modifyPassword', tags=['user'], description="修改密码", summary="修改个人密码")(modify_password)
router.patch('/user/active', tags=['user'], description="禁止登陆", summary="禁用或启用账户")(forbbiden_account)
router.patch('/user/delete', tags=['user'], description="删除用户", summary="伪删除用户")(delete_account)
