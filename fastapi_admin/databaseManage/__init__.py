# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/4 15:31
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

from sqlalchemy import create_engine
from fastapi_admin.auth.models import Base
# 所有model的基类，相当于django的Model
import databases

__all__ = ['AdminDatabase']


class AdminDatabase():
    """
    主要用于数据库的管理
        1、创建异步数据库操作的database
        2、提供数据库migrate功能
        3、
    """
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.database_url = kwargs['database_url']
            cls.database = databases.Database(cls.database_url)
        return cls.__instance

    def create_all(self):
        """创建所有model的table"""
        engine = create_engine(self.database_url, )
        Base.metadata.create_all(bind=engine)

    async def startup(self):
        print("异步数据库连接")
        await self.database.connect()

    async def shutdown(self):
        print("异步数据库关闭连接")
        await self.database.disconnect()
