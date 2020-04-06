# -*- encoding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2020/4/1 0:33
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""


# 数据库配置
DATABASES = {
        'NAME': "fastapiadmin",
        'USER': "root",
        'PASSWORD': 'mnbvcxz123',
        'HOST': "localhost",
        'PORT': 3306,
        'ENGINE': "mysql+pymysql"
}
# SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}/{}?charset=utf8mb4".format(DATABASES.get('ENGINE'), DATABASES.get('USER'),
#                                                                     DATABASES.get('PASSWORD'), DATABASES.get('HOST'),
#                                                                     DATABASES.get('NAME'))
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"