# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/4/1 0:29
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.WxSh.models import ServiceProviders, BusinessManager
from fastapi_admin import FastAPIAdmin
from settings import SQLALCHEMY_DATABASE_URL
# CORS
origins = ['*']
app = FastAPI(debug=True)
#配置跨域
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
admin = FastAPIAdmin(app, SQLALCHEMY_DATABASE_URL)
# 注册所有需要创建基本方法的Model
from apps.AdminManager.models import AccountBook, AccountBookLog, Member

# admin.create_database()
admin.register_Model(AccountBook, need_user=True,get_need_user=True)
admin.register_Model(AccountBookLog,methods=['GET'], need_user=True,get_need_user=True)
# admin.register_Model(Member, need_user=True)
admin.register_Model(Member, methods=["GET", "POST","DELETE","PUT"],need_user=True,get_need_user=True)
admin.register_Model(ServiceProviders,)
admin.register_Model(BusinessManager)
admin.create_database()
# res_model = get_res_schema(schema=UserSchema)
# app.get('/test_page',response_model=res_model)(page_query(User,))
from apps.AdminManager.views import router

app.include_router(router)

from fastapi_admin import AdminDatabase
from fastapi_admin.auth.models import  User
@app.get('/register_user',deprecated=True)
async  def start():
    """初始化用户信息的，请勿调用"""
    users_query=User.__table__.select()
    default_member=Member(member_name="默认会员",rate=0)
    default_member.id= await AdminDatabase().database.execute(Member.__table__.insert().values(member_name="默认会员",rate='0'))
    users=await AdminDatabase().database.fetch_all(users_query)
    for user in users:
        await AdminDatabase().database.execute( AccountBook.__table__.insert().values(user_id=user.id,member_id=default_member.id))
    return {"code":0}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8031)
