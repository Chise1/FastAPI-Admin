# -*- encoding: utf-8 -*-
"""
@File    : database_func.py
@Time    : 2020/4/3 13:18
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :记录注册的类需要的数据库的方法
"""

async def startup(database):
    await database.connect()


async def shutdown(database):
    await database.disconnect()