# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/3 0:01
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :默认的view类
"""
import copy
from typing import Optional, Dict, List,Union

from fastapi import Body


class BaseView:
    """该类为抽象类，需要继承并实现相关功能"""
    list_display: Union[List[str], str] = "__all__"

    def __init__(self, model=None, database=None, schema=None, **kwargs):
        """
        初始化基于类的视图,
            注意：可以先初始化，并实现所有的功能之后，在调用之前一定要将model、database、schema补齐
        :param model: 操作的sqlalchemy的Model
        :param database: 操作数据库的database
        :param schema: 用作数据验证的schema
        """
        self.model = model
        self.table=model.__table__
        self.database = database
        self.schema = schema
        for k, v in kwargs.items():
            setattr(self, k, v)
        async def update(instance: schema = Body(..., )):
            res = copy.deepcopy(instance)
            # id = instance.pop('id')
            query = self.table.filter(id=instance.id).update(instance)
            await database.execute(query)
            return res
        self.update = update
        async def create(instance: schema = Body(..., )):
            query = self.table.create(instance)
            return await database.execute(query)
        self.create = create
        async def delete(instance: schema = Body(..., )):
            query = self.table.delete(instance)
            return await database.execute(query)
        self.delete = delete

    def get_list_display(self) -> List[str]:
        """获取类对应要展示的数字,默认为list_display"""
        return self.list_display

    async def list(self):
        """
        get
        :return:
        """
        if self.get_list_display() == "__all__":
            query = self.table.select()
        else:
            query = self.table.select(*self.get_list_display())
        return await self.database.fetch_all(query)

    async def startup(self):
        print("连接数据库了")
        await self.database.connect()

    async def shutdown(self):
        print("关闭数据库了")
        await self.database.disconnect()