# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/5 11:00
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :权限先关的schema
"""
from pydantic import BaseModel
from .models import User
class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    is_active: bool
    is_superuser: bool
class UserDB(UserSchema):
    pass
from pydantic import EmailStr
class UserInDb(UserDB):
    email:EmailStr

class TokenData(BaseModel):
    username: str = None

class Token(BaseModel):
    access_token: str
    token_type: str