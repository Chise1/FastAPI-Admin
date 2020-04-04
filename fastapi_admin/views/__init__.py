# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/4 18:40
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import List, Union, Set
from fastapi import Body


class BaseView:
    """该类为抽象类，需要继承并实现相关功能"""
    list_display: Union[List[str], str] = "__all__"
    methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE')
    def __init__(self, model, schema, database=None, **kwargs):
        """
        初始化基于类的视图,
            注意：可以先初始化，并实现所有的功能之后，在调用之前一定要将model、database、schema补齐
        :param model: 操作的sqlalchemy的Model
        :param database: 操作数据库的database
        :param schema: 用作数据验证的schema
        """
        self.model = model
        self.table = model.__table__
        self.database = database
        self.schema = schema
        for k, v in kwargs.items():
            setattr(self, k, v)

        async def update(id, instance: schema = Body(..., )):
            query = self.table.update().where(self.model.id == id).values(**dict(instance))
            return await database.execute(query)

        self.update = update

        async def create(instance: schema = Body(..., )):
            query = self.table.insert().values(dict(instance))
            return await database.execute(query)

        self.create = create

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

    async def retrieve(self, id):
        """返回一个类型的详情"""
        query = self.table.select().where(self.model.id == id)
        print(query)
        return await self.database.fetch_one(query)

    async def delete(self, id):
        query = self.table.delete().where(self.model.id == id)
        return await self.database.execute(query)
