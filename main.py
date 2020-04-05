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
from fastapi_admin import FastAPIAdmin
from database import engine
from apps.Admin import views, models
from settings import SQLALCHEMY_DATABASE_URL

crud = views
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

admin = FastAPIAdmin(app, SQLALCHEMY_DATABASE_URL)
# 注册所有需要创建基本方法的Model
# admin.register_Model(UserTest)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, )