# -*- encoding: utf-8 -*-
"""
@File    : databases.py
@Time    : 2020/4/1 0:31
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :sqlalchemy需要的一些初始化操作
"""
# 导入settings的数据库设置
from settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine(SQLALCHEMY_DATABASE_URL, )
# 该类的每个实例将是一个数据库会话。该类本身还不是数据库会话。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 所有model的基类，相当于django的Model
Base = declarative_base()
