# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/4/1 0:29
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List
import requests
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from apps.Admin.models import UserTest
from fastapi_admin import FastAPIAdmin
from database import SessionLocal, engine
from apps.Admin import views, models, schemas
from settings import SQLALCHEMY_DATABASE_URL

crud = views
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
# def get_db():
#     try:
#         db = SessionLocal()
#         print("我创建了")
#         yield db
#         print("我执行了了")
#     finally:
#         print("我关闭了")
#         db.close()
# from  apps.Admin.models import Item
# # User.__model__.write2route('/user',app,User,get_db = SessionLocal())
# # Item.__model__.write2route('/get_item',app,Item,db = SessionLocal())
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/read_users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
# # SchemaUser=get_schema(User)
# #
# # @app.post('/test_get_schema',response_model=List[SchemaUser])
# # async def test_read_users(db: Session = Depends(get_db),item:SchemaUser=Body(...,)):
# #     """
# #     测试自动生成的schema
# #     :param db:
# #     :return:
# #     """
# #     print(item.test())
# #     print(item.test_view())
# #     ret= db.query(Item).all()
# #     return ret


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
# 创建并注册admin类
admin = FastAPIAdmin(app, SQLALCHEMY_DATABASE_URL)
# 注册所有需要创建基本方法的Model
admin.register_Model(UserTest)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, )
