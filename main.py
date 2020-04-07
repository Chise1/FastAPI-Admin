# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/4/1 0:29
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import math
from typing import Dict, List

from fastapi import FastAPI
from pydantic import Field
from sqlalchemy import select, func

from fastapi_admin import FastAPIAdmin, User, AdminDatabase, create_schema
from fastapi_admin.auth.schemas import UserSchema
from fastapi_admin.publicDepends.paging_query import page_query, get_res_schema
from settings import SQLALCHEMY_DATABASE_URL

app = FastAPI(debug=False)

admin = FastAPIAdmin(app, SQLALCHEMY_DATABASE_URL)
# 注册所有需要创建基本方法的Model
from apps.AdminManager.models import AccountBook, AccountBookLog, Member
# admin.create_database()
admin.register_Model(AccountBook, need_user=True)
admin.register_Model(AccountBookLog, need_user=True)
admin.register_Model(Member, need_user=True)
res_model=get_res_schema(schema=UserSchema)
admin.create_database()
app.get('/test_page',response_model=res_model)(page_query(User,))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8031 )
